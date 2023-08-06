"""接口基础类"""

import polars as pl
from typing import Optional, Union, Dict
from vxquant.model.preset import vxMarketPreset
from vxquant.model.exchange import (
    vxOrder,
    vxAccountInfo,
    vxPosition,
    vxCashPosition,
    vxTrade,
    vxTransferInfo,
)
from vxquant.model.contants import (
    OrderDirection,
    OrderOffset,
    OrderStatus,
    OrderType,
    SecType,
)
from vxutils import vxAPIWrappers


class vxMdAPI(vxAPIWrappers):
    __defaults__ = {
        "current": {"class": "vxquant.providers.tdx.MultiTdxHQProvider", "params": {}},
        "calendar": {
            "class": "vxquant.providers.spiders.calendar_sse.CNCalenderProvider",
            "params": {},
        },
        "instruments": {
            "class": "vxquant.providers.local.vxLocalInstrumentsProvider",
            "params": {},
        },
        "features": {
            "class": "vxquant.providers.local.vxLocalFeaturesProvider",
            "params": {},
        },
    }



class vxTdAPI(vxAPIWrappers):
    """交易接口类"""

    __defaults__ = {
        "current": {"class": "vxquant.providers.tdx.TdxHQProvider", "params": {}},
        "get_account": {},
        "get_positions": {},
        "get_orders": {},
        "get_execution_reports": {},
        "order_batch": {},
        "order_cancel": {},
    }

    def __init__(self, **providers: Union[str, Dict]) -> None:
        super().__init__(**providers)

    def order_volume(
        self,
        symbol: str,
        volume: int,
        price: Optional[float] = 0,
        account_id: str = None,
    ) -> vxOrder:
        """下单

        Arguments:
            account_id {str} -- _description_
            symbol {str} -- _description_
            volume {int} -- _description_
            price {Optional[float]} -- _description_ (default: {None})

        Returns:
            vxorder {vxOrder} -- 下单委托订单号
        """
        if volume == 0:
            raise ValueError("volume can't be 0.")

        if (
            not price
            and vxMarketPreset(symbol).security_type == SecType.BOND_CONVERTIBLE
        ):
            ticks = self.current(symbol)
            price = ticks[symbol].ask1_p if volume > 0 else ticks[symbol].bid1_p

        vxorder = vxOrder(
            account_id=account_id,
            symbol=symbol,
            volume=abs(volume),
            price=price,
            order_offset=OrderOffset.Open if volume > 0 else OrderOffset.Close,
            order_direction=OrderDirection.Buy if volume > 0 else OrderDirection.Sell,
            order_type=OrderType.Market if price <= 0 else OrderType.Limit,
            status=OrderStatus.PendingNew,
        )

        ret_orders = self.order_batch(vxorder)
        return ret_orders[0]
