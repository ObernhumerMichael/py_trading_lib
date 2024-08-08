from typing import List

from py_trading_lib.analysis import *

__all__ = ["AnalysisHandler"]


class AnalysisHandler:
    def __init__(self) -> None:
        self._technical_indicators: List[TechnicalIndicator] = []
        self._conditions: List[Condition] = []
        self._signals: List[Signal] = []

    def add_ti(self, ti: TechnicalIndicator) -> List[str]:
        self._technical_indicators.append(ti)
        return ti.get_indicator_names()

    def add_condition(self, condition: Condition) -> str:
        self._conditions.append(condition)
        return condition.get_condition_name()

    def add_signal(self, signal: Signal):
        self._signals.append(signal)
