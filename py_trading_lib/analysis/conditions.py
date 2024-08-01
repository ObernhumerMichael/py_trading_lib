from abc import ABC, abstractmethod
from typing import Literal, TypeAlias, Union, Callable

import pandas as pd

operators: TypeAlias = Literal["<", "<=", ">", ">=", "=="]
comparison_types: TypeAlias = Union[float, int, str]


class ICondition(ABC):
    @abstractmethod
    def is_condition_true(self, data: pd.DataFrame) -> pd.Series:
        pass

    @abstractmethod
    def get_condition_name(self) -> str:
        pass


class CheckRelation(ICondition):
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

    def is_condition_true(self, data: pd.DataFrame) -> pd.Series:
        return self.relation.is_condition_true(data)

    def get_condition_name(self) -> str:
        return self.relation.get_condition_name()


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

    def get_condition_name(self):
        return self.condition_name


class _NumericRelation(_Relation, ICondition):
    def is_condition_true(self, data: pd.DataFrame) -> pd.Series:
        result: pd.Series = self.check_relation(
            data[self.indicator_name], self.comparison_value
        )
        result.name = self.get_condition_name()
        return result


class _StringRelation(_Relation, ICondition):
    def is_condition_true(self, data: pd.DataFrame) -> pd.Series:
        result: pd.Series = self.check_relation(
            data[self.indicator_name], data[self.comparison_value]
        )
        result.name = self.get_condition_name()
        return result
