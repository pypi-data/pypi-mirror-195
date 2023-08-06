"""因子构建类"""
import re
import polars as pl
from tqdm import tqdm
from typing import Dict, List, Union
from vxquant.model.typehint import DateTimeType
from vxquant.model.instruments import vxInstruments
from vxquant.apis import vxMdAPI
from vxquant.factor.expr.ops import *
from vxutils import vxtime, to_datetime, logger


def to_expr(name: str, feature: str = None, groupby: str = None) -> pl.Expr:
    """将字符串公式转化为pl的表达式格式

    Arguments:
        name {str} -- 名字
        feature {str} -- _description_

    Returns:
        _type_ -- _description_
    """
    # Following patterns will be matched:
    # - $close -> Feature("close")
    # - $close5 -> Feature("close5")
    # - $open+$close -> Feature("open")+Feature("close")
    # TODO: this maybe used in the feature if we want to support the computation of different frequency data
    # - $close@5min -> Feature("close", "5min")

    if feature is None:
        feature = name

    # Chinese punctuation regex:
    # \u3001 -> 、
    # \uff1a -> ：
    # \uff08 -> (
    # \uff09 -> )
    chinese_punctuation_regex = r"\u3001\uff1a\uff08\uff09"
    for pattern, new in [
        (
            rf"\$\$([\w{chinese_punctuation_regex}]+)",
            r'PFeature("\1")',
        ),  # $$ must be before $
        (rf"\$([\w{chinese_punctuation_regex}]+)", r'pl.col("\1")'),
        # (r"(\w+\s*)\(", r"Operators.\1("),
    ]:  # Features  # Operators
        feature = re.sub(pattern, new, feature)

    return (
        eval(feature).alias(name)
        if groupby is None
        else eval(feature).over(groupby).alias(name)
    )


class vxFactorBuilder:
    def __init__(
        self,
        mdapi: vxMdAPI,
        instruments: Union[str, vxInstruments],
        start_date: DateTimeType = None,
        end_date: DateTimeType = None,
        fields: List[str] = None,
    ):
        if isinstance(instruments, str):
            instruments = mdapi.instruments(instruments)
        self.start_date = to_datetime(start_date or "2005-01-01")
        self.end_date = to_datetime(end_date or vxtime.today())
        self._mdapi = mdapi
        self._instruments = instruments
        self._features = self._mdapi.features(
            instruments.all_instruments(),
            self.start_date,
            self.end_date,
            "1d",
            fields,
        ).lazy()

    def exclude_instruments(
        self, instruments: Union[str, vxInstruments]
    ) -> "vxFactorBuilder":
        """排除股票池中的股票

        Arguments:
            instruments {vxInstruments} -- 股票池

        Returns:
            vxFactorBuilder -- _description_
        """
        if isinstance(instruments, str):
            instruments = self._mdapi.instruments(instruments)
        self._instruments.difference(instruments)
        logger.info(f"剔除股票池: {instruments._name}")
        return self

    @property
    def _instruments_filter(self) -> pl.DataFrame:
        trade_dates = self._mdapi.calendar(self.start_date, self.end_date)
        instruments_filters = []
        instruments_rows = []
        cnt = 0
        for trade_date in tqdm(trade_dates, f"构建股票池过滤器{self._instruments._name}"):
            available_symbols = self._instruments.list_instruments(trade_date)
            instruments_rows.extend(
                [
                    {"trade_date": trade_date, "symbol": symbol, "mask": True}
                    for symbol in available_symbols
                ]
            )
            cnt += len(available_symbols)
            if cnt > 100_000:
                instruments_filters.append(pl.DataFrame(instruments_rows))
                instruments_rows = []
                cnt = 0
        if instruments_rows:
            instruments_filters.append(pl.DataFrame(instruments_rows))

        return pl.concat(instruments_filters)

    def build_on_timeseries(self, **factor_exprs: Dict[str, str]) -> "vxFactorBuilder":
        """基于时序构建因子

        Arguments:
            factor_exprs {dict} -- 因子定义表达式如: MA20="Mean($close,20)",EMA20="EMA($close, 20)" ...

        Returns:
            vxFactorBuilder --
        """

        with vxtime.timeit(f"基于时序构建因子: {len(factor_exprs)}"):
            self._features = self._features.with_columns(
                [
                    to_expr(name, factor_expr, groupby="symbol")
                    for name, factor_expr in factor_exprs.items()
                ]
            )

        return self

    def build_on_sectors(self, **factor_exprs: Dict[str, str]) -> "vxFactorBuilder":
        """基于横截面构建因子

        Arguments:
            factor_exprs {dict} -- 因子定义表达式如: MA20="Mean($close,20)",EMA20="EMA($close, 20)" ...

        """
        with vxtime.timeit(f"基于横截面构建因子: {len(factor_exprs)}"):
            self._features = self._features.with_columns(
                [
                    to_expr(name, factor_expr, groupby="trade_date")
                    for name, factor_expr in factor_exprs.items()
                ]
            )

        return self

    def collect(self, *factor_names: List[str]) -> pl.DataFrame:
        if len(factor_names) == 1 and isinstance(factor_names[0], list):
            factor_names = factor_names[0]

        factor_cols = (
            pl.col(set("trade_date", "symbol", *factor_names))
            if factor_names
            else pl.col("*")
        )
        instruments_filter = self._instruments_filter
        with vxtime.timeit("计算因子...", show_title=True):
            features = self._features.collect()

        with vxtime.timeit("过滤股票池..."):
            return instruments_filter.join(
                features, on=["trade_date", "symbol"], how="left"
            ).select(factor_cols)


if __name__ == "__main__":
    mdapi = vxMdAPI()
    cnstock = mdapi.instruments("cnstock")
    newstock = mdapi.instruments("newstock")

    fbuilder = vxFactorBuilder(mdapi, "cnstock", "2005-01-04", "2023-03-01")
    fbuilder.exclude_instruments(newstock)
    fbuilder.build_on_timeseries(
        vxAlpha001="EMA(($close/$yclose)/$amount,20)/Std(($close/$yclose)/$amount,20)"
    )
    factor_data = fbuilder.collect()
    factor_data.write_parquet("./dist/factor.parquet")
