from typing import List

import pytest
import pandas as pd

from py_trading_lib.analysis.conditions import CheckRelation, ICondition


@pytest.fixture(autouse=True)
def sample_data():
    return pd.DataFrame({"a": [1, 2, 3], "b": [3, 2, 1]})


class TestCondition:
    @pytest.mark.parametrize(
        "condition, expected",
        [
            (CheckRelation("a", "<", 2), [True, False, False]),
            (CheckRelation("a", ">", 2), [False, False, True]),
            (CheckRelation("a", "<=", 2), [True, True, False]),
            (CheckRelation("a", ">=", 2), [False, True, True]),
            (CheckRelation("a", "==", 2), [False, True, False]),
            (CheckRelation("a", "<", "b"), [True, False, False]),
            (CheckRelation("a", ">", "b"), [False, False, True]),
            (CheckRelation("a", "<=", "b"), [True, True, False]),
            (CheckRelation("a", ">=", "b"), [False, True, True]),
            (CheckRelation("a", "==", "b"), [False, True, False]),
        ],
    )
    def test_is_condition_true(
        self, condition: ICondition, expected: List[bool], sample_data
    ):
        result = condition.is_condition_true(sample_data)
        result = result.tolist()

        assert result == expected

    @pytest.mark.parametrize(
        "condition, expected",
        [
            (CheckRelation("a", "<", 2), "a<2"),
            (CheckRelation("a", ">", 2), "a>2"),
            (CheckRelation("a", "<=", 2), "a<=2"),
            (CheckRelation("a", ">=", 2), "a>=2"),
            (CheckRelation("a", "==", 2), "a==2"),
            (CheckRelation("a", "<", "b"), "a<b"),
            (CheckRelation("a", ">", "b"), "a>b"),
            (CheckRelation("a", "<=", "b"), "a<=b"),
            (CheckRelation("a", ">=", "b"), "a>=b"),
            (CheckRelation("a", "==", "b"), "a==b"),
        ],
    )
    def test_condition_name_of_result(
        self, condition: ICondition, expected: List[bool], sample_data
    ):
        result = condition.is_condition_true(sample_data)
        name = result.name

        assert name == expected

    @pytest.mark.parametrize(
        "condition, expected",
        [
            (CheckRelation("a", "<", 2), "a<2"),
            (CheckRelation("a", ">", 2), "a>2"),
            (CheckRelation("a", "<=", 2), "a<=2"),
            (CheckRelation("a", ">=", 2), "a>=2"),
            (CheckRelation("a", "==", 2), "a==2"),
            (CheckRelation("a", "<", "b"), "a<b"),
            (CheckRelation("a", ">", "b"), "a>b"),
            (CheckRelation("a", "<=", "b"), "a<=b"),
            (CheckRelation("a", ">=", "b"), "a>=b"),
            (CheckRelation("a", "==", "b"), "a==b"),
        ],
    )
    def test_get_condition_name(self, condition: ICondition, expected: List[bool]):
        name = condition.get_condition_name()

        assert name == expected
