"""供应接口"""

import pandas as pd
import polars as pl
from abc import ABC, abstractmethod
from typing import Dict, List, Union, Optional
from pathlib import Path
from vxutils import vxtime, vxLRUCache, to_datetime, diskcache, to_timestamp, logger
from vxsched import vxEvent, vxTrigger
from vxquant.model.exchange import (
    vxAccountInfo,
    vxPosition,
    vxCashPosition,
    vxOrder,
    vxTrade,
)
from vxquant.model.instruments import vxInstruments
from vxquant.model.typehint import DateTimeType, InstrumentType
from vxquant.model.exchange import vxTick
from vxsched.context import vxContext


ProviderContext = vxContext()


class vxHQProvider(ABC):
    context = ProviderContext
    _tickcache = vxLRUCache()

    def __call__(self, *symbols: List[InstrumentType]) -> Dict[InstrumentType, vxTick]:
        """实时行情接口

        Returns:
            Dict[InstrumentType, vxTick] -- _description_
        """
        if len(symbols) == 1 and isinstance(symbols[0], list):
            symbols = symbols[0]

        ticks = {}
        _missing_symbols = []
        for symbol in symbols:
            if symbol in self._tickcache:
                ticks[symbol] = self._tickcache[symbol]
            else:
                _missing_symbols.append(symbol)

        if _missing_symbols:
            ticks = self._hq(*_missing_symbols)
            self._tickcache.update(ttl=3, **ticks)

        return {
            symbol: self._tickcache[symbol]
            for symbol in symbols
            if symbol in self._tickcache
        }

    @abstractmethod
    def _hq(self, *symbols: List[InstrumentType]) -> Dict[InstrumentType, vxTick]:
        """实时数据接口

        Returns:
            Dict[InstrumentType, vxTick] -- 返回值样例:
            {
                "SHSE.600000": vxTick(...),
                "SHSE.600001": vxTick(...),
                ...
            }
        """
        pass


class vxCalendarProvider(ABC):
    context = ProviderContext

    def __call__(
        self,
        start_date: DateTimeType = None,
        end_date: DateTimeType = None,
        market: str = "cn",
    ):
        start_date = to_datetime(start_date or "2010-01-01")
        end_date = to_datetime(end_date or vxtime.today())

        if f"calendar_{market}" not in diskcache:
            dates = self.get_trade_dates(market)
            diskcache.set(
                f"calendar_{market}", dates, to_timestamp(dates[-1]) - vxtime.now()
            )

        trade_days = diskcache[f"calendar_{market}"]

        return (
            pl.DataFrame({"trade_date": trade_days})
            .with_columns([pl.col("trade_date").apply(to_datetime)])
            .filter((pl.col("trade_date").is_between(start_date, end_date)))
            .sort(by="trade_date")["trade_date"]
        )

    def get_trade_dates(self, market: str = "cn") -> List[InstrumentType]:
        """获取该市场全部日历 --- 2010年1月1日以来的所有交易日历

        Arguments:
            market {str} -- 市场代码

        Returns:
            List[InstrumentType] -- 返回值: ['2022-01-01', '2022-01-02', ...]
        """


class vxInstrumentsProvider(ABC):
    context = ProviderContext

    def __call__(self, instruments_name: str = "all") -> vxInstruments:
        """获取相关股票池的证券

        Keyword Arguments:
            instruments_name {str} -- 股票池名称，可以为指数代码、证券行业代码、股票池类型(index,industry ) (default: {"all" -- 所有股票})

        Returns:
            vxInstruments -- _description_
        """
        raise NotImplementedError


class vxFeaturesProvider(ABC):
    context = ProviderContext

    def __call__(
        self,
        instruments: List[InstrumentType],
        start_date: DateTimeType = None,
        end_date: DateTimeType = None,
        freq: str = "1d",
        features: List[str] = None,
    ) -> pl.DataFrame:
        """获取行情通用接口

        Arguments:
            instruments {List[InstrumentType]} -- 需要下载的证券类型
            features: List[str] -- 行情列表
            freq: str -- 行情周期，只支持: {'1d'/'1min'}
            start_date {DateTimeType} -- 开始时间
            end_date {DateTimeType} -- 结束时间

        Returns:
            pl.DataFrame -- 返回： [trade_date, symbol, open, high, low, close, yclose, volume, amount, turnover_rate, volume_ratio,openinerest] 的列表
        """
        raise NotImplementedError


class vxFactorsProvider:
    context = ProviderContext

    def __init__(self, features: Union[pl.DataFrame, pd.DataFrame]) -> None:
        if isinstance(features, pd.DataFrame):
            features = pl.from_pandas(features)
        self._features = features
        self._instruments = self._features["symbol"].unique().to_list()
        self._trade_dates = self._features["trade_dates"].unique().sort().to_list()

    def __call__(
        self,
        instruments: List[InstrumentType],
        start_date: DateTimeType = None,
        end_date: DateTimeType = None,
        freq: str = "1d",
        factors: List[str] = None,
    ) -> pl.DataFrame:
        start_date = to_datetime(start_date or "2005-01-01")
        end_date = to_datetime(end_date or vxtime.today())
        freq = "day" if freq == "1d" else "min"
        factors = factors or "*"

        return (
            self._db.filter(
                (pl.col("symbol").is_in(instruments))
                & (pl.col("trade_date").is_between(start_date, end_date))
            )
            .collect()
            .select(pl.col(factors))
        )

    def update_factors(self, factors: pl.DataFrame) -> None:
        """保存因子数据

        Arguments:
            factor {pl.DataFrame} -- factor： "trade_date", "symbol", "factor1","factor2"...
        """
        if isinstance(factors, pl.DataFrame):
            factors = factors.lazy()
        self._db = self._db.join(factors, on=["trade_date", "symbol"])


class vxGetAccountProvider(ABC):
    context = ProviderContext

    def __call__(self, account_id: str = None) -> vxAccountInfo:
        """获取账户信息接口

        Keyword Arguments:
            account_id {str} -- 账号信息 (default: {None})

        Returns:
            vxAccountInfo -- 返回 vxaccountinfo对应的信息
        """
        raise NotImplementedError


class vxGetPositionsProvider(ABC):
    context = ProviderContext

    def __call__(
        self,
        symbol: InstrumentType = None,
        acccount_id: str = None,
    ) -> Dict[InstrumentType, Union[vxPosition, vxCashPosition]]:
        """获取持仓信息接口

        Keyword Arguments:
            symbol {InstrumentType} -- 持仓证券信息 (default: {None})
            acccount_id {str} -- 账号信息 (default: {None})

        Returns:
            Dict[InstrumentType, Union[vxPosition, vxCashPosition]] -- 返回{symbol: vxposition}的字典
        """
        raise NotImplementedError


class vxGetOrdersProvider(ABC):
    context = ProviderContext

    def __call__(
        self, account_id: str = None, filter_finished: bool = True
    ) -> Dict[str, vxOrder]:
        """获取委托订单接口

        Keyword Arguments:
            account_id {str} -- 账号 (default: {None})
            filter_finished {bool} -- 是否过滤已完成委托订单 (default: {True})


        Returns:
            Dict[str, vxOrder] -- 返回{order_id: vxorder}的字典
        """
        raise NotImplementedError


class vxGetExecutionReportsProvider(ABC):
    context = ProviderContext

    def __call__(
        self, account_id: str = None, order_id: str = None, trade_id: str = None
    ) -> Dict[str, vxTrade]:
        """获取成交信息接口

        Keyword Arguments:
            account_id {str} -- 账号 (default: {None})
            order_id {str} -- 委托订单号 (default: {None})
            trade_id {str} -- 成交编号 (default: {None})

        Returns:
            Dict[str, vxTrade] -- 返回{trade_id: vxtrade}的字典
        """
        raise NotImplementedError


class vxOrderBatchProvider(ABC):
    context = ProviderContext

    def __call__(self, *vxorders) -> List[vxOrder]:
        """批量委托下单接口

        Keyword Arguments:
            vxorders {vxOrder} -- 待提交的委托信息

        Returns:
            List[vxOrder] -- 返回提交成功的vxorders，并且将order.exchange_order_id字段予以赋值
        """
        raise NotImplementedError


class vxOrderCancelProvider(ABC):
    context = ProviderContext

    def __call__(self, *vxorders) -> None:
        """批量撤单接口

        Keyword Arguments:
            vxorders {vxOrder} -- 待取消的委托信息，取消委托中order.exchange_order_id字段若为空，则跳过
        """
        raise NotImplementedError


class vxPublisherProvider(ABC):
    """发布器"""

    context = ProviderContext

    def __init__(self, channel_name: str) -> None:
        self._channel_name = channel_name

    @property
    def channel_name(self) -> str:
        """消息通道名称"""
        return self._channel_name

    def __str__(self) -> str:
        return f"< {self.__class__.__name__}({self.channel_name})"

    __repr__ = __str__

    @abstractmethod
    def __call__(
        self,
        event: Union[str, vxEvent],
        data="",
        trigger: Optional[vxTrigger] = None,
        priority: float = 10,
        channel: str = None,
        **kwargs,
    ) -> None:
        """发布消息

        Arguments:
            event {Union[str, vxEvent]} -- 要推送消息或消息类型
            data {Any} -- 消息数据信息 (default: {None})
            trigger {Optional[vxTrigger]} -- 消息触发器 (default: {None})
            priority {int} -- 优先级，越小优先级越高 (default: {10})
        """


class vxSubscriberProvider(ABC):
    """订阅器"""

    context = ProviderContext

    def __init__(self, channel_name: str) -> None:
        self._channel_name = channel_name

    @property
    def channel_name(self) -> str:
        """消息通道名称"""
        return self._channel_name

    def __str__(self) -> str:
        return f"< {self.__class__.__name__}({self.channel_name})"

    @abstractmethod
    def __call__(self, callback=None) -> List[vxEvent]:
        pass


if __name__ == "__main__":
    from vxquant.model.nomalize import to_symbol

    with vxtime.timeit():
        f = vxFactorsProvider(
            "/Users/libao/src/开源代码/vxquant/.data/cn/day_stock_factors.parquet"
        )
        df = f.database.with_columns(
            [
                pl.col("ts_code").apply(to_symbol),
                pl.col("total_mv").log().alias("market_cap"),
                (1 / pl.col("pb")).alias("bm"),
            ]
        ).collect()

        print(df)
        df.select(pl.exclude("ts_code")).write_parquet(
            "/Users/libao/src/开源代码/vxquant/.data/cn/day_stock_factors.parquet"
        )
