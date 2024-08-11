import pytest

import pandas as pd

from py_trading_lib.utils.utils import *
from py_trading_lib.utils.utils import select_only_needed_cols


@pytest.mark.parametrize(
    "input", [pd.Series([1, 2, 3]), pd.DataFrame({"a": [1, 2, 3]})]
)
def test_convert_to_df_from_sr_or_df_pass(input):
    result = convert_to_df_from_sr_or_df(input)
    assert isinstance(result, pd.DataFrame)


def test_convert_to_df_from_sr_or_df_fail():
    with pytest.raises(TypeError):
        convert_to_df_from_sr_or_df("invalid")


@pytest.mark.parametrize(
    "input, expected",
    [
        (pd.Series([1, 2, 3]), True),
        (pd.DataFrame({"a": [1, 2, 3]}), True),
        (1, False),
    ],
)
def test_is_series_or_dataframe(input, expected: bool):
    assert is_series_or_dataframe(input) == expected


def test_select_only_needed_cols_pass():
    expected_selection = pd.DataFrame({"a": [1, 2, 3]})
    data = {"a": [1, 2, 3], "b": [7, 8, 9]}
    df = pd.DataFrame(data)

    selection = select_only_needed_cols(["a"], df)

    pd.testing.assert_frame_equal(selection, expected_selection)


def test_select_only_needed_cols_fail():
    data = {"a": [1, 2, 3], "b": [7, 8, 9]}
    df = pd.DataFrame(data)

    with pytest.raises(KeyError):
        select_only_needed_cols(["z"], df)
