from abc import ABC, abstractmethod
from typing import Literal, TypeAlias, Union, Callable, List

import pandas as pd

import py_trading_lib.utils.sanity_checks as sanity
import py_trading_lib.utils.utils as utils

operators: TypeAlias = Literal["<", "<=", ">", ">=", "=="]
comparison_types: TypeAlias = Union[float, int, str]

__all__ = ["Condition", "CheckRelation", "CheckAllTrue"]


class Condition(ABC):
    def calculate(self, data: pd.DataFrame) -> pd.Series:
        self._perform_sanity_checks(data)
        condition = self._try_calculate(data)
        return condition

    @abstractmethod
    def _perform_sanity_checks(self, data: pd.DataFrame) -> None:
        sanity.check_not_empty(data)

    def _try_calculate(self, data: pd.DataFrame) -> pd.Series:
        try:
            condition = self._calculate(data)
            condition.name = self.get_name()
        except Exception as e:
            raise RuntimeError(
                f"Something went wrong during the calculation of the condition: {self.get_name()}."
            ) from e

        return condition

    @abstractmethod
    def _calculate(self, data: pd.DataFrame) -> pd.Series:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass


class CheckRelation(Condition):
    def __init__(
        self,
        indicator_name: str,
        operator: Literal["<", "<=", ">", ">=", "=="],
        comparison_value: Union[float, int, str],
    ) -> None:
        if isinstance(comparison_value, (float, int)):
            self.relation = _NumericRelation(indicator_name, operator, comparison_value)
        elif isinstance(comparison_value, str):
            self.relation = _StringRelation(indicator_name, operator, comparison_value)

    def _calculate(self, data: pd.DataFrame) -> pd.Series:
        return self.relation._calculate(data)

    def _perform_sanity_checks(self, data: pd.DataFrame) -> None:
        super()._perform_sanity_checks(data)
        self.relation._perform_sanity_checks(data)
        self._check_contains_only_numbers_and_nans(data)

    def _check_contains_only_numbers_and_nans(self, data: pd.DataFrame):
        nan_free_data = data.dropna()
        sanity.check_contains_only_numbers(nan_free_data)

    def get_name(self) -> str:
        return self.relation.get_name()


class _Relation:
    def __init__(
        self,
        indicator_name: str,
        operator: operators,
        comparison_value: comparison_types,
    ) -> None:
        self.indicator_name = indicator_name
        self.operator = operator
        self.comparison_value = comparison_value
        self.check_relation = self.get_operator_func(operator)
        self.condition_name = (
            f"{self.indicator_name}{self.operator}{self.comparison_value}"
        )

    def get_operator_func(self, operator: operators) -> Callable:
        operators = {
            "<": lambda x, y: x < y,
            "<=": lambda x, y: x <= y,
            ">": lambda x, y: x > y,
            ">=": lambda x, y: x >= y,
            "==": lambda x, y: x == y,
        }
        if operator not in operators:
            raise ValueError(f"Invalid relational operator: {operator}")
        return operators[operator]

    def get_name(self):
        return self.condition_name


class _NumericRelation(_Relation, Condition):
    def _calculate(self, data: pd.DataFrame) -> pd.Series:
        result: pd.Series = self.check_relation(
            data[self.indicator_name], self.comparison_value
        )
        result.name = self.get_name()
        return result

    def _perform_sanity_checks(self, data: pd.DataFrame) -> None:
        indicator = [self.indicator_name]
        sanity.check_cols_exist_in_df(indicator, data)


class _StringRelation(_Relation, Condition):
    def _calculate(self, data: pd.DataFrame) -> pd.Series:
        result: pd.Series = self.check_relation(
            data[self.indicator_name], data[self.comparison_value]
        )
        result.name = self.get_name()
        return result

    def _perform_sanity_checks(self, data: pd.DataFrame) -> None:
        indicators = [self.indicator_name, self.comparison_value]
        sanity.check_cols_exist_in_df(indicators, data)


class CheckAllTrue(Condition):
    def __init__(self, conditions: List[str]):
        self._conditions = conditions

    def _perform_sanity_checks(self, data: pd.DataFrame) -> None:
        super()._perform_sanity_checks(data)

        self._check_conditions_empty()
        sanity.check_cols_exist_in_df(self._conditions, data)

        needed_data = self._select_only_needed_cols(data)
        sanity.check_contains_only_bools(needed_data)

    def _check_conditions_empty(self) -> None:
        if len(self._conditions) == 0:
            raise ValueError("The there must be at least one condition to be checked.")

    def _select_only_needed_cols(self, df: pd.DataFrame) -> pd.DataFrame:
        selection = df[self._conditions]
        selection = utils.convert_to_df_from_sr_or_df(selection)
        return selection

    def _calculate(self, data: pd.DataFrame) -> pd.Series:
        data_to_calc = self._select_only_needed_cols(data)
        signal = data_to_calc.all(axis=1)
        signal = self._validate(signal)
        return signal

    def _validate(self, signal: pd.Series | bool) -> pd.Series:
        if isinstance(signal, pd.Series):
            return signal
        else:
            raise TypeError("The calculted result is not a pandas Series.")

    def get_name(self) -> str:
        return f"CheckAllTrue={self._conditions}"
