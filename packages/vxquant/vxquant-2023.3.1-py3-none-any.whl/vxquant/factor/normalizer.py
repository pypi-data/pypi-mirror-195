"""因子标准化"""

import polars as pl
from tqdm import tqdm
from typing import List, Any
from scipy.stats import linregress
from concurrent.futures import ThreadPoolExecutor as Executor


class vxFactorNormalizer:
    def __init__(self, factors: pl.DataFrame):
        self._factors = factors.drop_nulls()

    def fix_nan(
        self,
        factor_names: List[str] = None,
        method: str = "drop",
        fill_value: Any = None,
    ):
        """修复缺失值

        Arguments:
            factor_names {List[str]} -- 因子名称

        Keyword Arguments:
            method {str} -- 修复方法：drop / fill_mad / fill_mean / fill_forward (default: {"drop"})

        """
        pass

    def standardize(
        self, factor_names: List[str] = None, n: float = 3, method: str = "mad"
    ) -> "vxFactorNormalizer":
        """去极值以及标准化

        Keyword Arguments:
            factor_names {List[str]} -- 因子名称 (default: {None})
            n {float} -- 倍数 (default: {3})
            method {str} -- 去极值的方法 (mad or winsorize_std) (default: {"MAD"})

        Raises:
            ValueError: 不支持的去极值方法

        """
        if not factor_names:
            factor_names = self._factors.columns

        if method == "mad":

            def filter_extreme(factor_col) -> pl.Series:
                median = factor_col.median()
                new_median = (factor_col - median).abs().median()

                return factor_col.clip(
                    factor_col.median() - n * new_median,
                    factor_col.median() + n * new_median,
                )

        elif method == "winsorize_std":

            def filter_extreme(factor_cal) -> pl.Expr:
                return factor_cal.clip(
                    factor_cal.mean() - n * factor_cal.std(),
                    factor_cal.mean() + n * factor_cal.std(),
                ).over("trade_date")

        else:
            raise ValueError(f"filter extreme method: {method} 暂不支持")

        print("=" * 60)
        self._factors = self._factors.with_columns(
            pl.col(
                [
                    factor_name
                    for factor_name in factor_names
                    if factor_name not in ["trade_date", "symbol", "mask"]
                ]
            )
            .apply(filter_extreme)
            .over("trade_date")
        )
        self._factors = self._factors.with_columns(
            [
                (pl.col(factor_name) - pl.col(factor_name).mean())
                / pl.col(factor_name).std()
                for factor_name in factor_names
                if factor_name not in ["trade_date", "symbol", "mask"]
            ]
        )

        return self

    def neutralization(
        self, factor_names: List[str], neutralize_factors: pl.DataFrame
    ) -> "vxFactorNormalizer":
        x = neutralize_factors.select(
            [
                pl.col("trade_date", "symbol"),
                pl.concat_list(pl.exclude(["trade_date", "symbol"])).alias("x"),
            ]
        )
        factor_datas = self._factors.join(x, on=["trade_date", "symbol"], how="left")
        executor = Executor()
        import numpy as np

        with tqdm(total=len(factor_datas["trade_date"].unique())) as pbar:

            def _neutralize(group_df: pl.DataFrame) -> pl.DataFrame:
                x = group_df["x"]
                y = group_df["vxFactor001"]
                print(x, y)
                print(linregress(x, y))

                # print(group_df)
                # print(x)

                for name in factor_names:
                    # resi = linregress(x, group_df[name])
                    # print(resi)
                    print(name)
                # pbar.update(1)
                # return pl.DataFrame(
                #    dict(
                #        executor.map(
                #            lambda name: (
                #                name,
                #                linregress(x, group_df[name].to_numpy())[-1],
                #            ),
                #            factor_names,
                #        )
                #    )
                # ).vstack(group_df.select(["trade_date", "symbol"]), in_place=False)

            factor_datas.groupby("trade_date").apply(_neutralize)


if __name__ == "__main__":
    factor_data = pl.read_parquet("./dist/factor.parquet")
    print(factor_data.fill_null(strategy="backward"))
    normalizer = vxFactorNormalizer(factor_data)
    normalizer.standardize(["vxFactor001"])
    neutralize_factors = factor_data.select(["trade_date", "symbol", "amount"])
    normalizer.neutralization(["vxFactor001"], neutralize_factors)
    print(normalizer._factors)
