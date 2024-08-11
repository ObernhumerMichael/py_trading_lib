import pytest

import pandas as pd

from py_trading_lib.analysis import *


@pytest.fixture
def example_analysis():
    analysis = Analysis()

    sma = analysis.add_ti(SMA(2))[0]
    relation = analysis.add_condition(CheckRelation(sma, ">", 2))
    analysis.set_signal(SignalAllConditionsTrue([relation]))

    return analysis


@pytest.fixture
def example_tohclv():
    tohclv = {
        "TIME": [1679144400000, 1679148000000, 1679151600000, 1679155200000],
        "OPEN": [1, 1, 1, 1],
        "HIGH": [1, 1, 1, 1],
        "LOW": [1, 1, 1, 1],
        "CLOSE": [1, 1, 10, 10],
        "VOLUME": [1, 1, 1, 1],
    }
    return pd.DataFrame(tohclv)


class TestAnalysis:
    def test_add_ti_return_name(self):
        analysis = Analysis()
        sma = SMA(10)
        expected = sma.get_names()

        name = analysis.add_ti(sma)

        assert name == expected

    def test_add_ti_list(self):
        analysis = Analysis()

        analysis.add_ti(SMA(10))

        assert len(analysis._technical_indicators) == 1

    def test_add_condition_return_name(self):
        analysis = Analysis()
        condition = CheckRelation("test", "<", 2)
        expected = condition.get_name()

        name = analysis.add_condition(condition)

        assert name == expected

    def test_add_signal_list(self):
        analysis = Analysis()
        signal = SignalAllConditionsTrue(["a"])

        analysis.set_signal(signal)

        assert analysis._signal is signal

    def test_calculate_signal_no_tohclv(
        self, example_analysis: Analysis, not_kline_data: pd.DataFrame
    ):
        with pytest.raises(ValueError):
            example_analysis.calculate_signal(not_kline_data)

    def test_calculate_signal(
        self, example_analysis: Analysis, example_tohclv: pd.DataFrame
    ):
        result = example_analysis.calculate_signal(example_tohclv)

        assert result.tolist() == [False, False, True, True]

    def test_calculate_analysis_data_cols(
        self, example_analysis: Analysis, example_tohclv: pd.DataFrame
    ):
        analysis_data = example_analysis.calculate_analysis_data(example_tohclv)
        expected_cols = [
            "TIME",
            "OPEN",
            "HIGH",
            "LOW",
            "CLOSE",
            "VOLUME",
            "SMA_2",
            "SMA_2>2",
            "SignalAllConditionsTrue",
        ]
        columns = analysis_data.columns.tolist()

        assert columns == expected_cols
