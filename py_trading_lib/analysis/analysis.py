from typing import List

import pandas as pd

from py_trading_lib.analysis import TechnicalIndicator, Condition, Signal
import py_trading_lib.utils.sanity_checks as sanity

__all__ = ["Analysis"]


class Analysis:
    def __init__(self) -> None:
        self._technical_indicators: List[TechnicalIndicator] = []
        self._conditions: List[Condition] = []
        self._signal: Signal

    def add_ti(self, ti: TechnicalIndicator) -> List[str]:
        self._technical_indicators.append(ti)
        return ti.get_names()

    def add_condition(self, condition: Condition) -> str:
        self._conditions.append(condition)
        return condition.get_name()

    def set_signal(self, signal: Signal) -> None:
        self._signal = signal

    def _perform_sanity_checks(self, tohlcv: pd.DataFrame) -> None:
        sanity.check_tohlcv(tohlcv)
        self._check_correct_setup()

    def _check_correct_setup(self) -> None:
        if not self._technical_indicators:
            raise ValueError(
                "A TechnicalIndicator must be set otherwise no signal can be generated."
            )
        if not self._conditions:
            raise ValueError(
                "A Condition must be set otherwise no signal can be generated."
            )
        if not isinstance(self._signal, Signal):
            raise ValueError(
                "A Signal must be set otherwise no calculation can be made."
            )

    def calculate_signal(self, tohlcv: pd.DataFrame) -> pd.Series:
        analysis_data = self.calculate_analysis_data(tohlcv)
        signal = analysis_data[self._signal.get_name()]
        if not isinstance(signal, pd.Series):
            raise TypeError("The expected signal was not a pandas Series.")
        return signal

    def calculate_analysis_data(self, tohlcv: pd.DataFrame) -> pd.DataFrame:
        self._perform_sanity_checks(tohlcv)
        analysis_data = self._calculate_technical_indicators(tohlcv)
        analysis_data = self._calculate_conditions(analysis_data)
        analysis_data = self._calculate_signal(analysis_data)
        return analysis_data

    def _calculate_technical_indicators(self, tohlcv: pd.DataFrame) -> pd.DataFrame:
        technical_indicators = [
            ti.calculate(tohlcv) for ti in self._technical_indicators
        ]
        return pd.concat([tohlcv] + technical_indicators, axis=1)

    def _calculate_conditions(self, analysis_data: pd.DataFrame) -> pd.DataFrame:
        conditions = [
            condition.calculate(analysis_data) for condition in self._conditions
        ]
        return pd.concat([analysis_data] + conditions, axis=1)

    def _calculate_signal(self, analysis_data: pd.DataFrame) -> pd.DataFrame:
        signal = self._signal.calculate(analysis_data)
        return pd.concat([analysis_data, signal], axis=1)
