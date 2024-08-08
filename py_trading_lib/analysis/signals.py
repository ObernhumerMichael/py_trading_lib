from abc import ABC, abstractmethod
from typing import List

import pandas as pd

import py_trading_lib.utils.sanity_checks as sanity

__all__ = ["Signal", "SignalAllConditionsTrue"]


class Signal(ABC):
    @abstractmethod
    def __init__(self, conditions: List[str]):
        self._conditions = conditions

    def calculate_signal(self, data: pd.DataFrame) -> pd.Series:
        self._perform_sanity_checks(data)
        data = self._select_only_needed_cols(data)

        signal = self._try_calculate_signal(data)

        return signal

    @abstractmethod
    def _perform_sanity_checks(self, data: pd.DataFrame) -> None:
        sanity.check_not_empty(data)
        sanity.check_cols_exist_in_df(self._conditions, data)
        sanity.check_contains_only_bools(data)

    def _select_only_needed_cols(self, df: pd.DataFrame) -> pd.DataFrame:
        selection = df[self._conditions]

        if not isinstance(selection, pd.DataFrame):
            raise TypeError("The selection of the conditions can only be a Dataframe")

        return selection

    def _try_calculate_signal(self, data) -> pd.Series:
        try:
            signal = self._calculate_signal(data)
        except Exception as e:
            raise RuntimeError(
                "Something went wrong during the calculation of the signal."
            ) from e

        return signal

    @abstractmethod
    def _calculate_signal(self, data: pd.DataFrame) -> pd.Series:
        pass


class SignalAllConditionsTrue(Signal):
    def __init__(self, conditions: List[str]):
        super().__init__(conditions)

    def _perform_sanity_checks(self, data: pd.DataFrame) -> None:
        return super()._perform_sanity_checks(data)

    def _calculate_signal(self, data: pd.DataFrame) -> pd.Series:
        signal = data.all(axis=1)
        return self._validate(signal)

    def _validate(self, signal: pd.Series | bool) -> pd.Series:
        if isinstance(signal, pd.Series):
            return signal
        else:
            raise TypeError("The calculted signal is not a pandas Series.")
