import os
from typing import Any, List

import pandas as pd

__all__ = [
    "check_cols_for_tohlcv",
    "check_is_list1_in_list2",
    "check_has_min_len",
    "check_not_empty",
    "check_has_no_nans",
    "check_contains_only_bools",
    "check_contains_only_numbers",
    "check_file_exist",
    "check_is_file_csv",
]


def check_cols_for_tohlcv(klines: pd.DataFrame) -> None:
    required_cols = ["TIME", "OPEN", "HIGH", "LOW", "CLOSE", "VOLUME"]
    columns = klines.columns.tolist()

    if not _is_list1_in_list2(required_cols, columns):
        raise ValueError(
            f"The following columns must be present in the DataFrame: {required_cols}. Currently only the following are present: {columns}"
        )


def check_is_list1_in_list2(list1: List[Any], list2: List[Any]):
    if not _is_list1_in_list2(list1, list2):
        raise ValueError(
            f"The list1 is not fully represented in list2. {list1}  \u2208 {list2}"
        )


def _is_list1_in_list2(list1: List[Any], list2: List[Any]) -> bool:
    return set(list1).issubset(set(list2))


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


def check_file_exist(path: str):
    if not os.path.exists(path):
        raise FileNotFoundError(f"The file on the path: {path} does not exist.")


def check_is_file_csv(path: str):
    if not path.endswith(".csv"):
        raise ValueError(f"The file one {path} is not a CSV file.")
