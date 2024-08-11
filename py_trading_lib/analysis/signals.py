from abc import ABC, abstractmethod
from typing import List

import pandas as pd

import py_trading_lib.utils.sanity_checks as sanity
import py_trading_lib.utils.utils as utils
from py_trading_lib.analysis.conditions import CheckAllTrue

__all__ = ["Signal", "SignalAllConditionsTrue"]


class Signal(ABC):
    @abstractmethod
    def __init__(self, conditions: List[str]):
        self._conditions = conditions

    def calculate(self, data: pd.DataFrame) -> pd.Series:
        self._perform_sanity_checks(data)
        signal = self._try_calculate(data)
        return signal

    @abstractmethod
    def _perform_sanity_checks(self, data: pd.DataFrame) -> None:
        sanity.check_not_empty(data)
        sanity.check_cols_exist_in_df(self._conditions, data)
        data = self._select_only_needed_cols(data)
        sanity.check_contains_only_bools(data)

    def _try_calculate(self, data) -> pd.Series:
        try:
            data = self._select_only_needed_cols(data)
            signal = self._calculate(data)
            signal.name = self.get_name()
        except Exception as e:
            raise RuntimeError(
                "Something went wrong during the calculation of the signal."
            ) from e

        return signal

    def _select_only_needed_cols(self, df: pd.DataFrame) -> pd.DataFrame:
        selection = df[self._conditions]
        selection = utils.convert_to_df_from_sr_or_df(selection)
        return selection

    @abstractmethod
    def _calculate(self, data: pd.DataFrame) -> pd.Series:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass


class SignalAllConditionsTrue(Signal):
    def __init__(self, conditions: List[str]):
        super().__init__(conditions)

    def _perform_sanity_checks(self, data: pd.DataFrame) -> None:
        return super()._perform_sanity_checks(data)

    def _calculate(self, data: pd.DataFrame) -> pd.Series:
        condition = CheckAllTrue(self._conditions)
        signal = condition._calculate(data)
        return signal

    def get_name(self) -> str:
        return "SignalAllConditionsTrue"
