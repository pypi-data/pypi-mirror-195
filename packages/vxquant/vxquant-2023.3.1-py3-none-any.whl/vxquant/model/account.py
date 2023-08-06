import polars as pl
from multiprocessing import Lock
from typing import Dict, Union
from vxquant.model.typehint import InstrumentType
from vxquant.model.preset import vxMarketPreset
from vxquant.model.exchange import (
    vxAccountInfo,
    vxPosition,
    vxCashPosition,
    vxOrder,
    vxTrade,
    vxTransferInfo,
)
from vxutils import vxAPIWrappers


class vxLogicAccounts(vxAPIWrappers):
    def __init__(self, **providers: Union[str, Dict]) -> None:
        super().__init__(**providers)
        self._accounts = pl.DataFrame(
            {field: [] for field in vxAccountInfo.__vxfields__}
        )
        self._positions = (
            None  # pl.DataFrame({field: [] for field in vxPosition.__vxfields__})
        )
        self._orders = pl.DataFrame({field: [] for field in vxOrder.__vxfields__})
        self._trades = pl.DataFrame({field: [] for field in vxTrade.__vxfields__})
        self._lock = Lock()

    def create_account(
        self, account_id: str, init_balance: float = 0.0
    ) -> vxAccountInfo:
        cash = vxCashPosition(account_id=account_id)
        if self._positions:
            self._positions.extend(pl.DataFrame([cash.message]))
        else:
            self._positions = pl.DataFrame([cash.message])
        self.deposit(account_id, init_balance)

    def get_accont(self, account_id: str = None) -> vxAccountInfo:
        account_info = vxAccountInfo(
            portfolio_id="",
            account_id=account_id,
            currency="CNY",
            deposit=0,
            withdraw=0,
            debt=0,
            balance=self._positions.filter(
                (pl.col("account_id") == account_id) & (pl.col("symbol") == "CNY")
            ),
            frozen=self._orders.filter(
                pl.col("status").is_in(
                    ["New", "PendingNew", "PartiallyFilled", "Unknown"]
                )
            ),
            margin_available=0,
            marketvalue=self._positions.filter(
                (pl.col("account_id") == account_id) & (pl.col("symbol") != "CNY")
            )["marketvalue"].sum(),
            # 浮动盈亏
            fnl=self._positions.filter(
                (pl.col("account_id") == account_id) & (pl.col("symbol") != "CNY")
            )["marketvalue"].sum(),
        )
        return account_info

    def deposit(self, account_id: str = None, amount: float = 0.0) -> vxTransferInfo:
        pass

    def withdraw(self, account_id: str = None, amount: float = 0.0) -> vxTransferInfo:
        pass

    def get_positions(
        self,
        symbol: str = None,
        account_id: str = None,
    ) -> Union[vxPosition, vxCashPosition]:
        pass

    def get_orders(
        self,
        order_id: str = None,
        exchange_order_id: str = None,
        account_id: str = None,
    ) -> Union[str, vxOrder]:
        pass

    def get_trades(
        self,
        order_id: str = None,
        trade_id: str = None,
        account_id: str = None,
    ) -> Union[str, vxTrade]:
        pass

    def on_order_status(self, vxorder: vxOrder) -> None:
        pass

    def on_execution_reports(self, vxtrade: vxTrade) -> None:
        pass

    def on_submit_order(self, vxorder: vxOrder) -> None:
        pass

    def on_settle(self) -> None:
        pass


if __name__ == "__main__":
    a = vxLogicAccounts()
    a.create_account("test", 1000000)
    print(a._positions)
