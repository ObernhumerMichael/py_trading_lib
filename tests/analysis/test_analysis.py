import pytest

import pandas as pd

from py_trading_lib.analysis import *


@pytest.fixture
def example_analysis():
    analysis = Analysis()

    sma = analysis.add_ti(SMA(2))[0]
    check_relation = analysis.add_condition(CheckRelation(sma, ">", 2))
    analysis.add_condition(CheckAllTrue([check_relation]))

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
    def test_add_ti(self):
        analysis = Analysis()

        analysis.add_ti(SMA(10))

        assert len(analysis._technical_indicators) == 1

    def test_add_ti_return_name(self):
        analysis = Analysis()
        sma = SMA(10)
        expected = sma.get_names()

        name = analysis.add_ti(sma)

        assert name == expected

    def test_add_condition(self):
        analysis = Analysis()

        analysis.add_condition(CheckAllTrue(["a"]))

        assert len(analysis._conditions) == 1

    def test_add_condition_return_name(self):
        analysis = Analysis()
        condition = CheckRelation("test", "<", 2)
        expected = condition.get_name()

        name = analysis.add_condition(condition)

        assert name == expected

    def test_calculate_analysis_data_cols(
        self, example_analysis: Analysis, example_tohclv: pd.DataFrame
    ):
        expected_cols = [
            "TIME",
            "OPEN",
            "HIGH",
            "LOW",
            "CLOSE",
            "VOLUME",
            "SMA_2",
            "SMA_2>2",
            "CheckAllTrue=['SMA_2>2']",
        ]

        analysis_data = example_analysis.calculate_analysis_data(example_tohclv)
        columns = analysis_data.columns.tolist()
        print(columns)

        assert columns == expected_cols
