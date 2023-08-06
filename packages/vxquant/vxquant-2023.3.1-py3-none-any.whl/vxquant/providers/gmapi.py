"""掘金量化tick行情数据"""

from typing import List, Dict, Union, Any
from vxquant.providers.base import ProviderContext
from vxquant.providers.base import (
    vxHQProvider,
    vxGetAccountProvider,
    vxGetExecutionReportsProvider,
    vxGetOrdersProvider,
    vxGetPositionsProvider,
    vxOrderBatchProvider,
    vxOrderCancelProvider,
)
from vxquant.model.tools.gmData import (
    gmTickConvter,
    gmAccountinfoConvter,
    gmCashPositionConvter,
    gmOrderConvter,
    gmPositionConvter,
    gmTradeConvter,
)
from vxquant.model.exchange import (
    vxTick,
    vxAccountInfo,
    vxCashPosition,
    vxPosition,
    vxOrder,
    vxTrade,
)
from vxquant.model.typehint import InstrumentType

try:
    from gm import api as gm_api

except ImportError as e:
    raise ImportError("掘金量化库并未安装，请使用pip install gm 安装") from e


def init_provider_context(gm_token: str = "", gmcontext: Any = None):
    ProviderContext["gmcontext"] = gmcontext
    gm_api.set_token(gm_token)


class vxGMHQProvider(vxHQProvider):
    _BATCH_SIZE = 100

    def __init__(self):
        gm_token = self.context.get("gm_token")
        if gm_token is not None:
            gm_api.set_token(gm_token)

    def _hq(self, *symbols: List[InstrumentType]) -> Dict[InstrumentType, vxTick]:
        allticks = []
        for i in range(0, len(symbols), self._BATCH_SIZE):
            gmticks = gm_api.current(symbols=symbols[i : i + self._BATCH_SIZE])
            allticks.extend(gmticks)

        return dict(map(lambda gmtick: gmTickConvter(gmtick, key="symbol"), gmticks))


class vxGMGetAccountProvider(vxGetAccountProvider):
    def __call__(self, account_id: str = None) -> vxAccountInfo:
        gmcash = self.context["gmcontext"].account(account_id).cash
        return gmAccountinfoConvter(gmcash)


class vxGMGetCreditAccountProvider(vxGetAccountProvider):
    def __call__(self, account_id: str = None) -> vxAccountInfo:
        gmcash = self.context["gmcontext"].account(account_id).cash
        return gmAccountinfoConvter(gmcash)


class vxGMGetPositionsProvider(vxGetPositionsProvider):
    def __call__(
        self, symbol: InstrumentType = None, acccount_id: str = None
    ) -> Dict[InstrumentType, Union[vxPosition, vxCashPosition]]:
        if symbol:
            gmposition = self.context["gmcontext"].account(acccount_id).position(symbol)
            return {symbol: gmPositionConvter(gmposition)} if gmposition else None

        gmcash = self.context.account(acccount_id).cash
        vxpositions = {"CNY": gmCashPositionConvter(gmcash)}
        gmpositions = self.context.account().positions()
        vxpositions.update(
            map(
                lambda gmposition: gmPositionConvter(gmposition, key="symbol"),
                gmpositions,
            )
        )

        return vxpositions


class vxGMGetOrdersProvider(vxGetOrdersProvider):
    def __call__(
        self, account_id: str = None, filter_finished: bool = True
    ) -> Dict[str, vxOrder]:
        gmorders = (
            gm_api.get_unfinished_orders() if filter_finished else gm_api.get_orders()
        )
        return dict(
            map(
                lambda gmorder: gmOrderConvter(gmorder, key="exchange_order_id"),
                gmorders,
            )
        )


class vxGMGetExecutionReportsProvider(vxGetExecutionReportsProvider):
    def __call__(
        self, account_id: str = None, order_id: str = None, trade_id: str = None
    ) -> Dict[str, vxTrade]:
        gmtrades = gm_api.get_execution_reports()
        if order_id:
            gmtrades = [
                gmtrade for gmtrade in gmtrades if gmtrade.cl_ord_id == order_id
            ]

        if trade_id:
            gmtrades = [gmtrade for gmtrade in gmtrades if gmtrade.exec_id == trade_id]

        return dict(
            map(lambda gmtrade: gmTradeConvter(gmtrade, key="trade_id"), gmtrades)
        )


class vxGMOrderBatchProvider(vxOrderBatchProvider):
    def __call__(self, *vxorders) -> List[vxOrder]:
        if len(vxorders) == 1 and isinstance(vxorders[0], list):
            vxorders = vxorders[0]

        gmorders = gm_api.order_batch(
            [
                {
                    "symbol": vxorder.symbol,
                    "volume": vxorder.volume,
                    "price": vxorder.price,
                    "side": vxorder.order_direction.value,
                    "order_type": vxorder.order_type.value,
                    "position_effect": vxorder.order_offset.value,
                    "order_business": gm_api.OrderBusiness_NORMAL,
                    "position_src": gm_api.PositionSrc_L1,
                }
                for vxorder in vxorders
            ]
        )
        for vxorder, gmorder in zip(vxorders, gmorders):
            vxorder.exchange_order_id = gmorder.cl_ord_id
        return vxorders


class vxGMCreditOrderBatchProvider(vxOrderBatchProvider):
    def __call__(self, *vxorders) -> List[vxOrder]:
        raise NotImplementedError


class vxGMOrderCancelProvider(vxOrderCancelProvider):
    def __call__(self, *vxorders) -> None:
        if len(vxorders) == 1 and isinstance(vxorders[0], list):
            vxorders = vxorders[0]

        wait_cancel_orders = [
            {"cl_ord_id": vxorder.exchange_order_id, "account_id": ""}
            for vxorder in vxorders
            if vxorder.exchange_order_id
        ]
        return gm_api.order_cancel(wait_cancel_orders)
