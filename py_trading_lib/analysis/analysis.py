from typing import List

import pandas as pd

from py_trading_lib.analysis import TechnicalIndicator, Condition
import py_trading_lib.utils.sanity_checks as sanity

__all__ = ["Analysis"]


class Analysis:
    def __init__(self) -> None:
        self._technical_indicators: List[TechnicalIndicator] = []
        self._conditions: List[Condition] = []

    def add_ti(self, ti: TechnicalIndicator) -> List[str]:
        self._technical_indicators.append(ti)
        return ti.get_names()

    def add_condition(self, condition: Condition) -> str:
        self._conditions.append(condition)
        return condition.get_name()

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

    def calculate_analysis_data(self, tohlcv: pd.DataFrame) -> pd.DataFrame:
        self._perform_sanity_checks(tohlcv)
        analysis_data = self._calculate_technical_indicators(tohlcv)
        analysis_data = self._calculate_conditions(analysis_data)
        return analysis_data

    def _calculate_technical_indicators(self, tohlcv: pd.DataFrame) -> pd.DataFrame:
        technical_indicators = [
            ti.calculate(tohlcv) for ti in self._technical_indicators
        ]
        return pd.concat([tohlcv] + technical_indicators, axis=1)

    def _calculate_conditions(self, analysis_data: pd.DataFrame) -> pd.DataFrame:
        for condition in self._conditions:
            condition_result = condition.calculate(analysis_data)
            analysis_data = pd.concat([analysis_data, condition_result], axis=1)
        return analysis_data
