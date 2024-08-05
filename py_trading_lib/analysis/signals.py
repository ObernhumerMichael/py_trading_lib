from abc import ABC, abstractmethod

import pandas as pd

import py_trading_lib.utils.sanity_checks as sanity

__all__ = ["Signal", "SignalAllConditionsTrue"]


class Signal(ABC):
    @abstractmethod
    def __init__(self, conditions: pd.DataFrame):
        self._conditions = conditions

    def calculate_signal(self) -> pd.Series:
        self._perform_sanity_checks()
        signal = self._try_calculate_signal()
        return signal

    @abstractmethod
    def _perform_sanity_checks(self) -> None:
        sanity.check_not_empty(self._conditions)
        sanity.check_contains_only_bools(self._conditions)

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

    def _perform_sanity_checks(self) -> None:
        return super()._perform_sanity_checks()

    def _calculate_signal(self) -> pd.Series:
        signal = self._conditions.all(axis=1)
        return self._validate(signal)

    def _validate(self, signal: pd.Series | bool) -> pd.Series:
        if isinstance(signal, pd.Series):
            return signal
        else:
            raise TypeError("The calculted signal is not a pandas Series.")
