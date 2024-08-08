import pytest

import pandas as pd

from py_trading_lib.utils.utils import *


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
