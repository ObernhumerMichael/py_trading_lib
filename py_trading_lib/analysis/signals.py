from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Any, List

import pandas as pd


class ISignal(ABC):
    _conditions: pd.DataFrame

    @abstractmethod
    def __init__(self, conditions: pd.DataFrame):
        self._conditions = conditions

    def is_signal_true(self) -> pd.Series:
        self._sanity_checks()

        result = self._try_calculate_signal()

        return result

    @abstractmethod
    def _sanity_checks(self) -> None:
        self._check_df_not_empty(self._conditions)
        self._check_df_only_bools(self._conditions)

    def _check_df_not_empty(self, df: pd.DataFrame):
        if len(df) == 0:
            raise ValueError(
                "The conditions must contain values otherwise a signal can not be created."
            )

    def _check_df_only_bools(self, df: pd.DataFrame):
        cols = self._get_colum_names(df)
        is_bool_mask = pd.DataFrame()

        for col in cols:
            col_bool_mask = df[col].map(type) == bool
            is_bool_mask = pd.concat([is_bool_mask, col_bool_mask], axis=1)

        is_only_bools = is_bool_mask.all(axis=None)

        if is_only_bools == False:
            raise ValueError("The conditions passed contain values other than bool.")

    def _get_colum_names(self, df: pd.DataFrame) -> List[str]:
        return df.columns.tolist()

    def _try_calculate_signal(self) -> pd.Series:
        try:
            signal = self._calculate_signal()
        except Exception as e:
            raise Exception(
                "Someting went wrong during the calculation of the signal." + str(e)
            )

        if not isinstance(signal, pd.Series):
            raise ValueError(
                "Someting went wrong during the calculation of the signal. The signal was not a pandas Series."
            )

        return signal

    @abstractmethod
    def _calculate_signal(self) -> Any:
        pass


class SignalAllConditionsTrue(ISignal):
    def __init__(self, conditions: pd.DataFrame):
        super().__init__(conditions)

    def _sanity_checks(self) -> None:
        return super()._sanity_checks()

    def _calculate_signal(self) -> Any:
        return self._conditions.all(axis=1)
