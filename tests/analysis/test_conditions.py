from typing import List

import pytest
import pandas as pd

from py_trading_lib.analysis.conditions import *


@pytest.fixture()
def sample_data():
    return pd.DataFrame({"a": [1, 2, 3], "b": [3, 2, 1]})


@pytest.fixture()
def sample_data_with_none():
    return pd.DataFrame({"a": [None, None, 3], "b": [None, 2, None]})


class TestCondition:
    @pytest.mark.parametrize(
        "condition",
        [
            CheckRelation("z", "<", 2),
            CheckRelation("a", "<", "z"),
            CheckRelation("z", "<", "a"),
        ],
    )
    def test_is_condition_true_invalid_condition(
        self, condition: Condition, sample_data: pd.DataFrame
    ):
        with pytest.raises(ValueError):
            condition.is_condition_true(sample_data)

    @pytest.mark.parametrize(
        "condition",
        [CheckRelation("z", "<", 2)],
    )
    def test_is_condition_true_no_data(self, condition: Condition):
        with pytest.raises(ValueError):
            condition.is_condition_true(pd.DataFrame())

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
        self, condition: Condition, expected: List[bool], sample_data
    ):
        result = condition.is_condition_true(sample_data)
        result = result.tolist()

        assert result == expected

    @pytest.mark.parametrize(
        "condition",
        [
            (CheckRelation("a", "<", "b")),
            (CheckRelation("a", ">", "b")),
            (CheckRelation("a", "<=", "b")),
            (CheckRelation("a", ">=", "b")),
            (CheckRelation("a", "==", "b")),
        ],
    )
    def test_is_string_condition_false_for_none(
        self, condition: Condition, sample_data_with_none
    ):
        expected = [False, False, False]

        result = condition.is_condition_true(sample_data_with_none)
        result = result.tolist()

        assert result == expected

    @pytest.mark.parametrize(
        "condition, expected",
        [
            (CheckRelation("a", "<", 2), [False, False, False]),
            (CheckRelation("a", ">", 2), [False, False, True]),
            (CheckRelation("a", "<=", 2), [False, False, False]),
            (CheckRelation("a", ">=", 2), [False, False, True]),
            (CheckRelation("a", "==", 2), [False, False, False]),
        ],
    )
    def test_is_number_condition_false_for_none(
        self, condition: Condition, expected: List[bool], sample_data_with_none
    ):
        result = condition.is_condition_true(sample_data_with_none)
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
    def test_get_name(self, condition: Condition, expected: str):
        name = condition.get_name()

        assert name == expected
