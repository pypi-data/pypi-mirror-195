"""MINI QMT Providers"""

from pathlib import Path
from typing import List, Dict, Union
from multiprocessing import Lock
from enum import Enum
from vxsched import vxContext
from vxquant.model.contants import OrderStatus, TradeStatus
from vxquant.model.typehint import InstrumentType
from vxquant.model.exchange import (
    vxCashPosition,
    vxPosition,
    vxTick,
    vxOrder,
    vxTrade,
    vxAccountInfo,
)

from vxquant.model.tools.qmtData import (
    qmtTickConvter,
    qmtOrderConvter,
    qmtPositionConvter,
    qmtTradeConvter,
    qmtCashPositionConvter,
    qmtAccountInfoConvter,
)
from vxquant.model.preset import vxMarketPreset
from vxquant.providers.base import (
    vxHQProvider,
    vxGetAccountProvider,
    vxGetPositionsProvider,
    vxOrderBatchProvider,
    vxOrderCancelProvider,
    vxGetExecutionReportsProvider,
    vxGetOrdersProvider,
    ProviderContext,
)

from vxsched import vxscheduler
from vxutils import vxtime, logger

try:
    from xtquant import xtdata
    from xtquant.xttype import StockAccount
    from xtquant.xttrader import XtQuantTrader, XtQuantTraderCallback
except ImportError as e:
    raise ImportError("xtquant未安装，请将QMT安装目录")


def to_qmt_symbol(symbol: InstrumentType):
    """将symbol(SHSE.600000) --> QMT的symbol格式(600000.SH)"""
    return f"{symbol[-6:]}.{symbol[:2]}"


class vxMiniQMTHQProvider(vxHQProvider):
    def _hq(self, *symbols: List[InstrumentType]) -> Dict[InstrumentType, vxTick]:
        if len(symbols) == 1 and isinstance(symbols[0], list):
            symbols = symbols[0]

        qmt_symbols = [to_qmt_symbol(symbol) for symbol in symbols]
        qmt_ticks = xtdata.get_full_tick(qmt_symbols)
        for k, v in qmt_ticks.items():
            v["symbol"] = k
        return dict(map(lambda x: qmtTickConvter(x, "symbol"), qmt_ticks.values()))


class vxMiniQMTGetAccountProvider(vxGetAccountProvider):
    def __call__(self, account_id: str = None) -> vxAccountInfo:
        acc_info = self.context.trader.query_stock_asset(self._account)
        if not acc_info:
            raise ConnectionError(f"无法获取账户信息，请检查连接. {acc_info}")

        qmt_positions = self.context.trader.query_stock_positions(self._account)
        fnl = sum(p.marketvalue - p.open_price * p.volume for p in qmt_positions)
        return qmtAccountInfoConvter(acc_info, fnl=fnl)


class vxMiniQMTGetPositionsProvider(vxGetPositionsProvider):
    def __call__(
        self, symbol: InstrumentType = None, acccount_id: str = None
    ) -> Dict[InstrumentType, Union[vxPosition, vxCashPosition]]:
        qmt_positions = self.context.trader.query_stock_positions(self.context.account)
        positions = dict(map(lambda x: qmtPositionConvter(x, "symbol"), qmt_positions))
        if symbol:
            return positions.pop(symbol, {})

        acc_info = self.context.trader.query_stock_asset(self.context.account)
        if not acc_info:
            raise ConnectionError(f"无法获取账户信息，请检查连接. {acc_info}")
        cash_position = qmtCashPositionConvter(acc_info)
        positions["CNY"] = cash_position
        return positions


class vxMiniQMTGetOrdersProvider(vxGetOrdersProvider):
    def __call__(
        self, account_id: str = None, filter_finished: bool = True
    ) -> Dict[str, vxOrder]:
        qmt_orders = self.context.trader.query_stock_orders(
            self.context.account, filter_finished
        )
        return dict(
            map(lambda order: qmtOrderConvter(order, "exchange_order_id"), qmt_orders)
        )


class vxMiniQMTGetExecutionReportsProvider(vxGetExecutionReportsProvider):
    def __call__(
        self, account_id: str = None, order_id: str = None, trade_id: str = None
    ) -> Dict[str, vxTrade]:
        qmt_trades = self.context.trader.query_stock_trades(self.context.account)
        return dict(map(lambda x: qmtTradeConvter(x, "trade_id"), qmt_trades))


class vxMiniQMTOrderBatchProvider(vxOrderBatchProvider):
    def __call__(self, *vxorders) -> List[vxOrder]:
        if len(vxorders) == 1 and isinstance(vxorders[0], list):
            vxorders = vxorders[0]

        for vxorder in vxorders:
            price_type = (
                11
                if vxorder.order_type.name == "Limit"
                else 42
                if vxorder.symbol[:2] == "SH"
                else 47
            )
            exchange_order_id = self.context.trader.order_stock(
                account=self.context.account,
                stock_code=to_qmt_symbol(vxorder.symbol),
                order_type=23 if vxorder.order_direction.name == "Buy" else 24,
                order_volume=vxorder.volume,
                price_type=price_type,
                price=vxorder.price,
                strategy_name=vxorder.algo_order_id,
                order_remark=vxorder.order_id,
            )
            if exchange_order_id <= 0:
                vxorder.status = "Rejected"
                continue

            vxorder.exchange_order_id = exchange_order_id
            vxorder.status = "New"
            self.context.broker_orders[exchange_order_id] = vxorder

        return vxorders


class vxMiniQMTOrderCancelProvider(vxOrderCancelProvider):
    def __call__(self, *vxorders) -> None:
        if len(vxorders) == 1 and isinstance(vxorders[0], list):
            vxorders = vxorders[0]

        for vxorder in vxorders:
            if not vxorder.exchange_order_id:
                continue

            seq = self.context.trader.cancel_order_stock_async(
                self._account, vxorder.exchange_order_id
            )
            if seq <= 0:
                logger.error(
                    f"委托订单:{vxorder.order_id} 撤单失败{vxorder.symbol} {vxorder.order_direction} {vxorder.volume}"
                )
        return


class QMTAccountStatus(Enum):
    INVALID = -1
    OK = 0
    WAITING_LOGIN = 1
    STATUSING = 2
    FAIL = 3
    INITING = 4
    CORRECTING = 5
    CLOSED = 6
    ASSIS_FAIL = 7
    DISABLEBYSYS = 8
    DISABLEBYUSER = 9


class vxQMTTraderCallback(XtQuantTraderCallback):
    lock = Lock()

    def __init__(self, context: vxContext = None) -> None:
        self._context = context
        if "broker_orders" not in self._context:
            self._context["broker_orders"] = {}

        if "broker_trades" not in self._context:
            self._context["broker_trades"] = {}

    @property
    def context(self) -> vxContext:
        return self._context

    def on_connected(self):
        """
        连接成功推送
        """
        logger.info("连接成功")
        vxscheduler.submit_events("on_connected")

    def on_disconnected(self):
        """
        连接状态回调
        :return:
        """
        logger.warning("连接断开")
        vxscheduler.submit_events("on_disconnected")

    def on_account_status(self, status):
        """
        账号状态信息推送
        :param response: XtAccountStatus 对象
        :return:
        """
        logger.info(
            "账户状态变更为:"
            f" {status.account_id} {status.account_type} {QMTAccountStatus(status.status)}"
        )
        vxscheduler.submit_event(
            "on_account_status",
            (status.account_id, status.account_type, QMTAccountStatus(status.status)),
        )

    def on_stock_asset(self, asset):
        """
        资金信息推送
        :param asset: XtAsset对象
        :return:
        """
        logger.info(
            f"on asset callback {asset.account_id}, {asset.cash}, {asset.total_asset}"
        )

    def on_stock_order(self, order):
        """
        委托信息推送
        :param order: XtOrder对象
        :return:
        """
        logger.debug(
            f"收到成交更新: {order.stock_code} {order.order_status} {order.order_sysid}"
        )
        vxorder = qmtOrderConvter(order)

        if vxorder.exchange_order_id not in self.context.broker_orders:
            with self.lock:
                self.context.broker_orders[vxorder.exchange_order_id] = vxorder
                logger.info(f"[新增] 委托订单{vxorder.exchange_order_id} 更新为: {vxorder}")
            vxscheduler.submit_event("on_broker_order_status", vxorder)
            return

        broker_order = self.context.broker_orders[vxorder.exchange_order_id]
        if broker_order.status in [
            OrderStatus.Filled,
            OrderStatus.Expired,
            OrderStatus.Rejected,
            OrderStatus.Canceled,
            OrderStatus.Suspended,
        ]:
            logger.debug(
                f"[忽略更新] 委托订单 {vxorder.exchange_order_id} "
                f" 当前状态:{broker_order.status} 须更新状态: {vxorder.status}"
            )
            return

        if broker_order.filled_volume > vxorder.filled_volume:
            logger.debug(
                f"[忽略更新] 委托订单 {vxorder.exchange_order_id} 当前已成交:"
                f" {broker_order.filled_volume} > 更新状态:{vxorder.filled_volume}"
            )
            return

        # 更新委托订单状态
        with self.lock:
            broker_order.status = vxorder.status
            broker_order.filled_volume = vxorder.filled_volume
            broker_order.filled_amount = vxorder.filled_amount
            broker_order.updated_dt = vxorder.updated_dt
            self.context.broker_orders[broker_order.exchange_order_id] = broker_order
            logger.info(f"[更新] 委托订单{vxorder.exchange_order_id} 更新为: {broker_order}")
        vxscheduler.submit_event("on_broker_order_status", broker_order)

    def on_stock_trade(self, trade):
        """
        成交信息推送
        :param trade: XtTrade对象
        :return:
        """
        logger.debug(
            f"收到成交信息: {trade.account_id}, {trade.stock_code}, {trade.order_id}"
        )
        vxtrade = qmtTradeConvter(trade)

        if vxtrade.status != TradeStatus.Trade:
            logger.warning(f"收到非成交的回报信息: {vxtrade}")
            return

        if vxtrade.trade_id in self.context.broker_trades:
            logger.warning("收到重复的委托订单信息")
            return

        # 调整当日手续费
        if vxtrade.commission == 0:
            _preset = vxMarketPreset(vxtrade.symbol)
            vxtrade.commission = max(
                (
                    vxtrade.price
                    * vxtrade.volume
                    * (
                        _preset.commission_coeff_peramount
                        if vxtrade.order_direction.name == "Buy"
                        else (
                            _preset.commission_coeff_peramount
                            + _preset.tax_coeff_peramount
                        )
                    )
                ),
                5,
            )

        with self.lock:
            self.context.broker_trades[vxtrade.trade_id] = vxtrade
            logger.info(f"收到成交回报信息: {vxtrade}")
        vxscheduler.submit_event("on_broker_execution_report", vxtrade)

    def on_stock_position(self, position):
        """
        持仓信息推送
        :param position: XtPosition对象
        :return:
        """
        logger.info(f"持仓信息推送: {position.stock_code}, {position.volume}")

    def on_order_error(self, order_error):
        """
        下单失败信息推送
        :param order_error:XtOrderError 对象
        :return:
        """

        if order_error.order_id not in self.context.broker_orders:
            logger.warning(
                f"下单失败: {order_error.order_id}, {order_error.error_id},"
                f" {order_error.error_msg}"
            )
            return

        with self.lock:
            broker_order = self.context.broker_orders[order_error.order_id]
            if broker_order.status in [
                OrderStatus.Filled,
                OrderStatus.Expired,
                OrderStatus.Rejected,
                OrderStatus.Canceled,
                OrderStatus.Suspended,
            ]:
                logger.debug(
                    f"[忽略更新] 委托订单 {order_error.exchange_order_id} "
                    f" 当前状态:{broker_order.status} 须更新状态: {order_error.error_msg}"
                )
                return

            broker_order.status = "Rejected"
            broker_order.reject_code = "UnknownOrder"
            broker_order.reject_reason = order_error.error_msg
        vxscheduler.submit_event("on_broker_order_status", broker_order)

    def on_order_stock_async_response(self, response):
        """
        :param response: XtOrderResponse 对象
        :return:
        """
        # with self.lock:
        #    vxorder = self.seq_mapping.get(response.seq, None)
        #    vxorder.exchange_order_id = response.order_id
        #    self.broker_orders[vxorder.exchange_order_id] = vxorder
        pass

    def on_smt_appointment_async_response(self, response):
        """
        :param response: XtAppointmentResponse 对象
        :return:
        """
        pass


def init_provider_context(
    miniqmt_path: Union[str, Path],
    account_id: str = None,
    account_type: str = "STOCK",
    callback: vxQMTTraderCallback = None,
) -> None:
    ProviderContext.account = StockAccount(account_id, account_type)
    ProviderContext.trader = XtQuantTrader(miniqmt_path, int(vxtime.now()))
    ProviderContext.trader.start()
    connect_result = ProviderContext.trader.connect()
    if connect_result != 0:
        raise ConnectionError(f"连接失败: {connect_result}")
    logger.info(f"trader 连接成功. {ProviderContext.trader}")

    ProviderContext.trader.register_callback(callback)
    subscribe_result = ProviderContext.trader.subscribe(ProviderContext.account)
    if subscribe_result != 0:
        raise ConnectionError(f"订阅失败: {subscribe_result}")
    logger.info(f"订阅账号回调信息: {ProviderContext.account}")

    with vxQMTTraderCallback.lock:
        qmt_orders = ProviderContext.trader.query_stock_orders(
            ProviderContext.account, False
        )
        callback.context.broker_orders = dict(
            map(lambda order: qmtOrderConvter(order, "exchange_order_id"), qmt_orders)
        )
        qmt_trades = ProviderContext.trader.query_stock_trades(ProviderContext.account)
        callback.context.broker_trades = dict(
            map(lambda x: qmtTradeConvter(x, "trade_id"), qmt_trades)
        )
        logger.info(f"更新委托订单{len(qmt_orders)}个, 更新成交回报:{len(qmt_trades)}个.")
