#  Copyright (c) 2022 by Amplo.

"""
Defines various pooling functions.
"""

from __future__ import annotations

from typing import Callable

import polars as pl
from polars import internals as pli

__all__ = ["POOL_FUNCTIONS", "pl_pool"]


def root_mean_square(column: str) -> pli.Expr:
    return pl.col(column).pow(2).mean().pow(0.5)


def sum_values(column: str) -> pli.Expr:
    return pl.col(column).sum()


def abs_energy(column: str) -> pli.Expr:
    return pl.col(column).dot(pl.col(column))


def abs_max(column: str) -> pli.Expr:
    return pl.col(column).abs().max()


def n_mean_crossings(column: str) -> pli.Expr:
    """
    Calculates the number of crossings of x on mean.
    A crossing is defined as two sequential values where the first value is lower than
    mean and the next is greater, or vice-versa.
    """
    return ((pl.col(column) - pl.col(column).mean()).sign().diff() != 0).sum()


def abs_sum_of_changes(column: str) -> pli.Expr:
    return pl.col(column).diff().abs().sum()


def mean_of_changes(column: str) -> pli.Expr:
    return pl.col(column).diff().mean()


def abs_mean_of_changes(column: str) -> pli.Expr:
    return pl.col(column).diff().abs().mean()


def cid_ce(column: str) -> pli.Expr:
    """Calculates an estimate for a time series complexity."""
    parsed = ((pl.col(column) - pl.col(column).mean()) / pl.col(column).std()).diff()
    return parsed.dot(parsed).sqrt()


def linear_trend(column: str) -> pli.Expr:
    """OLS coeff"""
    ind = (pl.col("index") + 1).alias(column)
    return (ind.max() * ind.dot(pl.col(column)) - pl.col(column).sum() * ind.sum()) / (
        ind.max() * ind.pow(2).sum() - ind.sum().pow(2)
    )


def linear_trend_bias(column: str) -> pli.Expr:
    """OLS bias"""
    return pl.col(column).mean() - linear_trend(column) * (pl.col("index") + 1).mean()


def linear_trend_error(column: str) -> pli.Expr:
    """Errors of OLS fit"""
    error = (
        pl.col(column)
        - linear_trend(column) * (pl.col("index") + 1)
        - linear_trend_bias(column)
    )
    return error.pow(2).sum()


def peak_loc(column: str, n: int) -> pli.Expr:
    """Returns the value of peak n

    The concatenation is necessary to handle missing peaks.
    This results in a value of -1
    """
    parsed = pl.col(column)
    peaks = parsed.diff().sign().diff() == -2
    return pl.arg_where(peaks.cumsum() == n).first().fill_null(0).apply(lambda x: x - 1)


def peak_val(column: str, n: int) -> pli.Expr:
    """Returns the location of peak n"""
    parsed = pl.col(column)
    return parsed.filter(pl.col("index") == peak_loc(column, n)).first().fill_null(-1.0)


# ----------------------------------------------------------------------
# Globals

POOL_FUNCTIONS: dict[str, Callable[..., pli.Expr]] = {
    # --- Basics ---
    "min": pl.min,
    "max": pl.max,
    "mean": pl.mean,
    "std": pl.std,
    "median": pl.median,
    "variance": pl.var,
    "kurtosis": pl.Expr.kurtosis,
    "skew": pl.Expr.skew,
    "root_mean_square": root_mean_square,
    "sum_values": sum_values,
    # --- Characteristics ---
    "entropy": pl.Expr.entropy,
    "abs_energy": abs_energy,
    "abs_max": abs_max,
    "linear_trend": linear_trend,
    "linear_trend_error": linear_trend_error,
    "n_mean_crossings": n_mean_crossings,
    # --- Difference ---
    "abs_sum_of_changes": abs_sum_of_changes,
    "mean_of_changes": mean_of_changes,
    "abs_mean_of_changes": abs_mean_of_changes,
    "cid_ce": cid_ce,
    "peak_1_loc": lambda x: peak_loc(x, 1),
    "peak_2_loc": lambda x: peak_loc(x, 2),
    "peak_3_loc": lambda x: peak_loc(x, 3),
    "peak_1_val": lambda x: peak_val(x, 1),
    "peak_2_val": lambda x: peak_val(x, 2),
    "peak_3_val": lambda x: peak_val(x, 3),
}
_EXTENDED_POOL_FUNCTIONS: dict[str, Callable[..., pli.Expr]] = {
    "first": pl.first,
    **POOL_FUNCTIONS,
}


def pl_pool(
    df: pl.DataFrame,
    column_name: str,
    window_size: int,
    func_str: str,
) -> pl.DataFrame:
    """
    Pools series data with given aggregation functions.

    Parameters
    ----------
    df : pl.DataFrame
        Dataframe to convert, containing log, index, column.
    col : str
        Column to be pooled.
    window_size : int
        Window size for pooling.
    func_str : str
        Name of the pooling function to be used.

    Returns
    -------
    pl.DataFrame
        Pooled data where each column name consists of the original series data name and
        its pooling function name (keys of `aggregation` parameter).
        When for example the series data name is "series" and one `aggregation` key is
        named "min", the resulting column is named "series__pool=min".
    """
    # Set defaults
    LOG, INDEX = "log", "index"

    # Input check
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' is missing.")
    if LOG not in df.columns or INDEX not in df.columns:
        raise ValueError(f"Index columns ('{LOG}' and/or '{INDEX}') are missing.")

    # Set pooling function and polars expression
    func = _EXTENDED_POOL_FUNCTIONS[func_str]
    alias = f"{column_name}__pool={func_str}"
    if func.__module__ == "polars.internals.expr.expr":
        expr = func(pl.col(column_name)).alias(alias)
    else:
        expr = func(column_name).alias(alias)

    # Pool, ensure column order and return
    pooled_df = (
        df.groupby_dynamic(INDEX, every=f"{window_size}i", by=LOG).agg(expr).fill_nan(0)
    )
    return pooled_df[[LOG, INDEX, alias]]
