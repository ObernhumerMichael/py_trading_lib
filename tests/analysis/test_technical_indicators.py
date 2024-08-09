import pytest
import pandas as pd

from py_trading_lib.analysis.technical_indicators import *


@pytest.fixture
def sma_5():
    return SMA(length=5)


@pytest.fixture
def expected_sma_calc_result_first_rows():
    expected = {
        "SMA_5": {
            0: None,
            1: None,
            2: None,
            3: None,
            4: 68573.926,
            5: 68416.868,
            6: 68454.034,
            7: 68370.88200000001,
            8: 68461.764,
            9: 68665.888,
        }
    }

    return pd.DataFrame(expected)


@pytest.fixture
def expected_sma_calc_result_last_rows():
    expected = {
        "SMA_5": {
            390: 70379.732,
            391: 70420.13200000001,
            392: 70391.14800000002,
            393: 70387.798,
            394: 70217.808,
            395: 70049.792,
            396: 70023.312,
            397: 69950.7,
            398: 69932.848,
            399: 70020.048,
        }
    }
    return pd.DataFrame(expected)


@pytest.fixture
def rsi_5():
    return RSI(length=5)


@pytest.fixture
def expected_rsi_calc_result_first_rows():
    expected = {
        "RSI_5": {
            0: None,
            1: None,
            2: None,
            3: None,
            4: None,
            5: 35.332323077916364,
            6: 49.57072006111343,
            7: 46.71703148837669,
            8: 47.32306135962863,
            9: 74.47905826387989,
        }
    }
    return pd.DataFrame(expected)


@pytest.fixture
def expected_rsi_calc_result_last_rows():
    expected = {
        "RSI_5": {
            390: 53.86134034862355,
            391: 46.112192250502986,
            392: 57.19580637283783,
            393: 49.78385796527404,
            394: 31.647873521228853,
            395: 27.789177311933095,
            396: 49.72131429324174,
            397: 51.679668251456135,
            398: 55.96375524572976,
            399: 52.80210296096537,
        }
    }
    return pd.DataFrame(expected)


class TestTechnicalIndicators:
    row_num = 10

    @pytest.mark.parametrize("ti", ["sma_5", "rsi_5"])
    def test_calc_no_klines(self, ti: TechnicalIndicator, request):
        ti = request.getfixturevalue(ti)

        with pytest.raises(ValueError):
            ti.calculate(pd.DataFrame())

    @pytest.mark.parametrize("ti", ["sma_5", "rsi_5"])
    def test_calc_insufficient_klines(
        self, ti: TechnicalIndicator, insufficient_klines: pd.DataFrame, request
    ):
        ti = request.getfixturevalue(ti)

        with pytest.raises(ValueError):
            ti.calculate(insufficient_klines)

    @pytest.mark.parametrize("ti", ["sma_5", "rsi_5"])
    def test_calc_data_not_klines(
        self, ti: TechnicalIndicator, not_kline_data: pd.DataFrame, request
    ):
        ti = request.getfixturevalue(ti)

        with pytest.raises(ValueError):
            ti.calculate(not_kline_data)

    @pytest.mark.parametrize(
        "ti, expected",
        [
            ("sma_5", "expected_sma_calc_result_first_rows"),
            ("rsi_5", "expected_rsi_calc_result_first_rows"),
        ],
    )
    def test_calc_result_first_rows(
        self, example_klines, ti: TechnicalIndicator, expected, request
    ):
        expected = request.getfixturevalue(expected)
        ti = request.getfixturevalue(ti)

        indicator = ti.calculate(tohlcv=example_klines)
        indicator = indicator.head(self.row_num)

        indicator = self._make_df_to_testable_dict(indicator)
        expected = self._make_df_to_testable_dict(expected)

        assert indicator == expected

    @pytest.mark.parametrize(
        "ti, expected",
        [
            ("sma_5", "expected_sma_calc_result_last_rows"),
            ("rsi_5", "expected_rsi_calc_result_last_rows"),
        ],
    )
    def test_calc_result_last_rows(
        self, example_klines, ti: TechnicalIndicator, expected, request
    ):
        expected = request.getfixturevalue(expected)
        ti = request.getfixturevalue(ti)

        indicator = ti.calculate(tohlcv=example_klines)
        indicator = indicator.tail(self.row_num)

        indicator = self._make_df_to_testable_dict(indicator)
        expected = self._make_df_to_testable_dict(expected)

        assert indicator == expected

    @pytest.mark.parametrize("ti, expected", [("sma_5", 5), ("rsi_5", 5)])
    def test_get_min_len(self, ti: TechnicalIndicator, expected, request):
        ti = request.getfixturevalue(ti)

        min_len = ti.get_min_len()

        assert min_len == expected

    @pytest.mark.parametrize(
        "ti, expected", [("sma_5", ["SMA_5"]), ("rsi_5", ["RSI_5"])]
    )
    def test_get_names(self, ti: TechnicalIndicator, expected, request):
        ti = request.getfixturevalue(ti)

        names = ti.get_names()

        assert names == expected

    @pytest.mark.parametrize(
        "ti",
        ["sma_5", "rsi_5"],
    )
    def test_get_names_equals_calculated_column_names(
        self, example_klines, ti: TechnicalIndicator, request
    ):
        ti = request.getfixturevalue(ti)
        indicator = ti.calculate(tohlcv=example_klines)

        calculated_names = indicator.columns.tolist()
        names = ti.get_names()

        assert calculated_names == names

    def _make_df_to_testable_dict(self, df: pd.DataFrame):
        df = df.dropna()
        testable_dict = df.to_dict()
        return testable_dict
