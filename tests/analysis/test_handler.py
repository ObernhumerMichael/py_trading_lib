import pandas as pd

from py_trading_lib.analysis import *


class TestAnalysisHandlerAdds:
    def test_add_ti_return_name(self):
        analysis = AnalysisHandler()
        sma = SMA(10)
        expected = sma.get_indicator_names()

        name = analysis.add_ti(sma)

        assert name == expected

    def test_add_ti_list(self):
        analysis = AnalysisHandler()

        analysis.add_ti(SMA(10))

        assert len(analysis._technical_indicators) == 1

    def test_add_condition_return_name(self):
        analysis = AnalysisHandler()
        condition = CheckRelation("test", "<", 2)
        expected = condition.get_condition_name()

        name = analysis.add_condition(condition)

        assert name == expected

    def test_add_signal_list(self):
        analysis = AnalysisHandler()

        analysis.add_signal(SignalAllConditionsTrue(pd.DataFrame()))

        assert len(analysis._signals) == 1
