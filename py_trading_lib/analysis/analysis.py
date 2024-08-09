from typing import List
import pandas as pd

from py_trading_lib.analysis import *
import py_trading_lib.utils.sanity_checks as sanity

__all__ = ["Analysis"]


class Analysis:
    def __init__(self) -> None:
        self._technical_indicators: List[TechnicalIndicator] = []
        self._conditions: List[Condition] = []
        self._signal: Signal

    def add_ti(self, ti: TechnicalIndicator) -> List[str]:
        self._technical_indicators.append(ti)
        return ti.get_indicator_names()

    def add_condition(self, condition: Condition) -> str:
        self._conditions.append(condition)
        return condition.get_condition_name()

    def set_signal(self, signal: Signal):
        self._signal = signal

    def _perform_sanity_checks(self, tohclv: pd.DataFrame) -> None:
        sanity.check_not_empty(tohclv)
        sanity.check_cols_for_tohlcv(tohclv)
        self._check_correct_setup()

    def _check_correct_setup(self):
        if len(self._technical_indicators) == 0:
            raise ValueError(
                "A TechnicalIndicator must be set otherwise no signal can be generated."
            )
        if len(self._conditions) == 0:
            raise ValueError(
                "A Condition must be set otherwise no signal can be generated."
            )
        if not isinstance(self._signal, Signal):
            raise ValueError(
                "A Signal must be set otherwise no calculation can be made."
            )

    def calculate(self, tohlcv: pd.DataFrame) -> pd.Series:
        self._perform_sanity_checks(tohlcv)
        technical_indicators = self._calculate_technical_indicators(tohlcv)
        raise NotImplementedError

    def _calculate_technical_indicators(self, tohlcv: pd.DataFrame) -> pd.DataFrame:
        calculated_tis: List[pd.DataFrame] = []
        for ti in self._technical_indicators:
            calculated_ti = ti.calculate(tohlcv)
            calculated_tis.append(calculated_ti)
        return pd.concat(calculated_tis)
