import pytest
from typing import Dict, List

import pandas as pd

from py_trading_lib.utils.sanity_checks import *
from py_trading_lib.utils.sanity_checks import check_cols_exist_in_df


@pytest.fixture
def extended_tohlcv():
    kline = {
        "TIME": [1],
        "OPEN": [1],
        "HIGH": [1],
        "LOW": [1],
        "CLOSE": [1],
        "VOLUME": [1],
        "EXTRA": [1],
    }
    return pd.DataFrame(kline)


def test_check_cols_for_tohlcv_fail(not_kline_data: pd.DataFrame):
    with pytest.raises(ValueError):
        check_cols_for_tohlcv(not_kline_data)


@pytest.mark.parametrize("klines", ["example_klines", "extended_tohlcv"])
def test_check_cols_for_tohlcv_pass(klines: str, request: pytest.FixtureRequest):
    tohlcv: pd.DataFrame = request.getfixturevalue(klines)

    check_cols_for_tohlcv(tohlcv)


def test_check_cols_exist_in_df_fail():
    df = pd.DataFrame({"a": [1, 2, 3]})

    with pytest.raises(ValueError):
        check_cols_exist_in_df(["z"], df)


def test_check_cols_exist_in_df_pass():
    df = pd.DataFrame({"a": [1, 2, 3], "b": [1, 2, 3]})

    check_cols_exist_in_df(["b"], df)


def test_check_has_min_len_fail(insufficient_klines: pd.DataFrame):
    min_len = 99999

    with pytest.raises(ValueError):
        check_has_min_len(insufficient_klines, min_len)


def test_check_has_min_len_pass(example_klines: pd.DataFrame):
    min_len = 10

    check_has_min_len(example_klines, min_len)


def test_check_not_empty_pass():
    df = pd.DataFrame({"a": [1, 2, 3], "b": [1, 2, 3]})

    check_not_empty(df)


def test_check_not_empty_fail():
    df = pd.DataFrame()

    with pytest.raises(ValueError):
        check_not_empty(df)


def test_check_has_no_nans_pass():
    df = pd.DataFrame({"a": [1, 2, 3], "b": [1, 2, 3]})

    check_has_no_nans(df)


def test_check_has_no_nans_fail():
    df = pd.DataFrame({"a": [1, 2, None], "b": [1, 2, 3]})
    with pytest.raises(ValueError):
        check_has_no_nans(df)


def test_check_contains_only_bools_pass():
    df = pd.DataFrame(
        {
            "a": [True, False],
            "b": [True, False],
        }
    )

    check_contains_only_bools(df)


@pytest.mark.parametrize(
    "data",
    [
        {"a": [True, None, False], "b": [True, True, True]},
        {"a": [True, 0, False], "b": [True, True, True]},
        {"a": [True, 1, False], "b": [True, True, True]},
        {"a": [True, 3.14, False], "b": [True, True, True]},
        {"a": [True, -3.14, False], "b": [True, True, True]},
        {"a": [True, "invalid", False], "b": [True, True, True]},
        {"a": [True, [True], False], "b": [True, True, True]},
        {"a": [True, {"invalid": -1}, False], "b": [True, True, True]},
    ],
)
def test_check_contains_only_bools_fail(data: Dict):
    df = pd.DataFrame(data)

    with pytest.raises(TypeError):
        check_contains_only_bools(df)


@pytest.mark.parametrize(
    "data",
    [
        {"a": [1], "b": [1]},
        {"a": [-1], "b": [-1]},
        {"a": [3.14], "b": [3.14]},
        {"a": [-3.14], "b": [-3.14]},
        {"a": [1, 3.14 - 1, -3.14], "b": [1, 3.14 - 1, -3.14]},
    ],
)
def test_check_contains_only_numbers_pass(data: List):
    df = pd.DataFrame(data)

    check_contains_only_numbers(df)


@pytest.mark.parametrize(
    "data",
    [
        {"a": [1, 3, "test"], "b": [1, 2, 3]},
        {"a": [1, 3, True], "b": [1, 1, 1]},
        {"a": [1, 3, [1]], "b": [1, 1, 1]},
        {"a": [1, 3, {"invalid": -1}], "b": [1, 1, 1]},
        {"a": [1, 3.14, "test"], "b": [1, 1, 1]},
        {"a": [1, 3.14, True], "b": [1, 1, 1]},
        {"a": [1, 3.14, [1]], "b": [1, 1, 1]},
        {"a": [1, 3.14, {"invalid": -1}], "b": [1, 1, 1]},
    ],
)
def test_check_contains_only_numbers_fail(data: Dict):
    df = pd.DataFrame(data)

    with pytest.raises(TypeError):
        check_contains_only_numbers(df)


def test_check_file_exist_pass():
    check_file_exist("./example_klines/BTC_USDT.csv")


def test_check_file_exist_fail():
    with pytest.raises(FileNotFoundError):
        check_file_exist("./file_does_not_exist")


def test_check_is_file_csv_pass():
    check_is_file_csv("./example_klines/BTC_USDT.csv")


def test_check_is_file_csv_fail():
    with pytest.raises(ValueError):
        check_is_file_csv("./README.md")


@pytest.mark.parametrize("list1", [[], [1, 2], [1, 2, 3]])
def test_check_is_list1_in_list2_pass(list1: List):
    check_is_list1_in_list2(list1, [1, 2, 3])


def test_check_is_list1_in_list2_fail():
    with pytest.raises(ValueError):
        check_is_list1_in_list2([1, 2, 3, 4], [1, 2])
