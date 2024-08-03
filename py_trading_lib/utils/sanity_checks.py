from typing import Any

import pandas as pd


def check_cols_for_tohlcv(klines: pd.DataFrame) -> None:
    required_cols = ["TIME", "OPEN", "HIGH", "LOW", "CLOSE", "VOLUME"]
    columns = klines.columns.tolist()
    cols_exist = set(required_cols).issubset(set(columns))

    if not cols_exist:
        raise ValueError(
            f"The following columns must be present in the DataFrame: {required_cols}. Currently only the following are present: {columns}"
        )


def check_has_min_len(df: pd.DataFrame, min_len: int) -> None:
    len_klines = len(df)

    if len_klines < min_len:
        raise ValueError(
            f"The klines have a length of {len_klines} and a min lenght of {min_len} is needed."
        )


def check_not_empty(df: pd.DataFrame) -> None:
    if df.empty:
        raise ValueError(
            "The DataFrame must contain values otherwise it can't be operated on."
        )


def check_has_no_nans(df: pd.DataFrame) -> None:
    is_na_map = df.isna()
    contains_na = is_na_map.any(axis=None)
    if contains_na == True:
        raise ValueError("The DataFrame contains NaN or None values.")


def check_contains_only_bools(df: pd.DataFrame) -> None:
    _check_contains_only_type(df, bool)


def _check_contains_only_type(df: pd.DataFrame, type: Any) -> None:
    column_types = df.dtypes
    is_correct_type = column_types.eq(type)
    all_correct_type = is_correct_type.all()

    if not all_correct_type:
        raise TypeError(f"The pandas DataFrame contains values other than {type}.")


def check_contains_only_numbers(df: pd.DataFrame) -> None:
    column_types = df.dtypes
    is_int64 = column_types == "int64"
    is_float64 = column_types == "float64"
    are_correct_types = is_int64 | is_float64

    all_correct_type = are_correct_types.all()

    if not all_correct_type:
        raise TypeError(
            f"The pandas DataFrame contains values other than int64 or float64."
        )

    check_has_no_nans(df)  # is needed because numpy.NaN is represented as float64
