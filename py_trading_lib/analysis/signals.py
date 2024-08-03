from abc import ABC, abstractmethod

import pandas as pd

from ..utils.sanity_checks import check_not_empty, check_contains_only_bools


class Signal(ABC):
    @abstractmethod
    def __init__(self, conditions: pd.DataFrame):
        self._conditions = conditions

    def calculate_signal(self) -> pd.Series:
        self._sanity_checks()
        signal = self._try_calculate_signal()
        return signal

    @abstractmethod
    def _sanity_checks(self) -> None:
        check_not_empty(self._conditions)
        check_contains_only_bools(self._conditions)

    def _try_calculate_signal(self) -> pd.Series:
        try:
            signal = self._calculate_signal()
        except Exception as e:
            raise RuntimeError(
                "Something went wrong during the calculation of the signal."
            ) from e

        return signal

    @abstractmethod
    def _calculate_signal(self) -> pd.Series:
        pass


class SignalAllConditionsTrue(Signal):
    def __init__(self, conditions: pd.DataFrame):
        super().__init__(conditions)

    def _sanity_checks(self) -> None:
        return super()._sanity_checks()

    def _calculate_signal(self) -> pd.Series:
        signal = self._conditions.all(axis=1)
        return self._validate(signal)

    def _validate(self, signal: pd.Series | bool) -> pd.Series:
        if isinstance(signal, pd.Series):
            return signal
        else:
            raise TypeError("The calculted signal is not a pandas Series.")
