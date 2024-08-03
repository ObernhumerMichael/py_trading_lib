from abc import ABC, abstractmethod

import pandas as pd


class ISignal(ABC):
    @abstractmethod
    def __init__(self, conditions: pd.DataFrame):
        self._conditions = conditions

    def is_signal_true(self) -> pd.Series:
        self._sanity_checks()
        signal = self._try_calculate_signal()
        return signal

    @abstractmethod
    def _sanity_checks(self) -> None:
        self._check_df_not_empty(self._conditions)
        self._check_df_only_bools(self._conditions)

    def _check_df_not_empty(self, df: pd.DataFrame) -> None:
        if df.empty:
            raise ValueError(
                "The conditions must contain values, otherwise a signal cannot be created."
            )

    def _check_df_only_bools(self, df: pd.DataFrame) -> None:
        column_types = df.dtypes
        all_bools = column_types.eq(bool).all()

        if not all_bools:
            raise ValueError("The conditions passed contain values other than bool.")

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


class SignalAllConditionsTrue(ISignal):
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
