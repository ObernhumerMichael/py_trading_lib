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


@pytest.fixture()
def sample_data_extended():
    return pd.DataFrame({"a": [1, 2, 3], "b": [3, 2, 1], "z": [100, 0, -100]})


@pytest.fixture
def sample_conditions():
    conditions = {
        "a": [True, True, False],
        "b": [True, False, False],
        "c": [True, False, False],
    }
    return pd.DataFrame(conditions)


@pytest.fixture
def sample_broken_conditions():
    conditions = {
        "a": [None, False, True],
        "b": [True, False, True],
        "c": [True, False, True],
    }
    return pd.DataFrame(conditions)


@pytest.fixture
def sample_extended_conditions():
    conditions = {
        "a": [True, True, True],
        "b": [True, True, True],
        "c": [True, True, True],
        "z": ["TEST", False, False],
    }
    return pd.DataFrame(conditions)


class TestConditionGeneral:
    @pytest.mark.parametrize(
        "condition",
        [
            CheckRelation("z", "<", 2),
            CheckRelation("a", "<", "z"),
            CheckRelation("z", "<", "a"),
            CheckAllTrue([]),
        ],
    )
    def test_calculate_invalid_condition(
        self, condition: Condition, sample_data: pd.DataFrame
    ):
        with pytest.raises(ValueError):
            condition.calculate(sample_data)

    @pytest.mark.parametrize(
        "condition",
        [
            CheckRelation("z", "<", 2),
            CheckAllTrue(["a", "b"]),
        ],
    )
    def test_calculate_no_data(self, condition: Condition):
        with pytest.raises(ValueError):
            condition.calculate(pd.DataFrame())

    @pytest.mark.parametrize(
        "signal, data_fix",
        [
            (CheckRelation("a", "==", "b"), "sample_conditions"),
            (CheckRelation("a", "==", "b"), "sample_broken_conditions"),
            (CheckAllTrue(["a", "b", "c"]), "sample_broken_conditions"),
        ],
    )
    def test_calculate_broken_data(
        self, signal: CheckAllTrue, data_fix: str, request: pytest.FixtureRequest
    ):
        data = request.getfixturevalue(data_fix)

        with pytest.raises(TypeError):
            signal.calculate(data)

    @pytest.mark.parametrize(
        "condition,data_fix, expected",
        [
            (CheckRelation("a", "<", 2), "sample_data", [True, False, False]),
            (CheckRelation("a", ">", 2), "sample_data", [False, False, True]),
            (CheckRelation("a", "<=", 2), "sample_data", [True, True, False]),
            (CheckRelation("a", ">=", 2), "sample_data", [False, True, True]),
            (CheckRelation("a", "==", 2), "sample_data", [False, True, False]),
            (CheckRelation("a", "<", "b"), "sample_data", [True, False, False]),
            (CheckRelation("a", ">", "b"), "sample_data", [False, False, True]),
            (CheckRelation("a", "<=", "b"), "sample_data", [True, True, False]),
            (CheckRelation("a", ">=", "b"), "sample_data", [False, True, True]),
            (CheckRelation("a", "==", "b"), "sample_data", [False, True, False]),
            (CheckAllTrue(["a", "b", "c"]), "sample_conditions", [True, False, False]),
        ],
    )
    def test_calculate_valid_data(
        self,
        condition: Condition,
        expected: List[bool],
        data_fix: str,
        request: pytest.FixtureRequest,
    ):
        data: pd.DataFrame = request.getfixturevalue(data_fix)

        result = condition.calculate(data)

        result = result.tolist()
        assert result == expected

    @pytest.mark.parametrize(
        "condition,data_fix, expected",
        [
            (CheckRelation("a", "<", 2), "sample_data_extended", [True, False, False]),
            (CheckRelation("a", ">", 2), "sample_data_extended", [False, False, True]),
            (CheckRelation("a", "<=", 2), "sample_data_extended", [True, True, False]),
            (CheckRelation("a", ">=", 2), "sample_data_extended", [False, True, True]),
            (CheckRelation("a", "==", 2), "sample_data_extended", [False, True, False]),
            (
                CheckRelation("a", "<", "b"),
                "sample_data_extended",
                [True, False, False],
            ),
            (
                CheckRelation("a", ">", "b"),
                "sample_data_extended",
                [False, False, True],
            ),
            (
                CheckRelation("a", "<=", "b"),
                "sample_data_extended",
                [True, True, False],
            ),
            (
                CheckRelation("a", ">=", "b"),
                "sample_data_extended",
                [False, True, True],
            ),
            (
                CheckRelation("a", "==", "b"),
                "sample_data_extended",
                [False, True, False],
            ),
            (
                CheckAllTrue(["a", "b", "c"]),
                "sample_extended_conditions",
                [True, True, True],
            ),
        ],
    )
    def test_calculate_use_only_expected_cols(
        self,
        condition: Condition,
        expected: List[bool],
        data_fix: str,
        request: pytest.FixtureRequest,
    ):
        data: pd.DataFrame = request.getfixturevalue(data_fix)

        result = condition.calculate(data)

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
            (CheckAllTrue(["a", "b"]), "CheckAllTrue=['a', 'b']"),
        ],
    )
    def test_get_name(self, condition: Condition, expected: str):
        name = condition.get_name()

        assert name == expected

    @pytest.mark.parametrize(
        "condition, data_fix, expected",
        [
            (CheckRelation("a", "<", 2), "sample_data", "a<2"),
            (CheckRelation("a", ">", 2), "sample_data", "a>2"),
            (CheckRelation("a", "<=", 2), "sample_data", "a<=2"),
            (CheckRelation("a", ">=", 2), "sample_data", "a>=2"),
            (CheckRelation("a", "==", 2), "sample_data", "a==2"),
            (CheckRelation("a", "<", "b"), "sample_data", "a<b"),
            (CheckRelation("a", ">", "b"), "sample_data", "a>b"),
            (CheckRelation("a", "<=", "b"), "sample_data", "a<=b"),
            (CheckRelation("a", ">=", "b"), "sample_data", "a>=b"),
            (CheckRelation("a", "==", "b"), "sample_data", "a==b"),
            (
                CheckAllTrue(["a", "b"]),
                "sample_conditions",
                "CheckAllTrue=['a', 'b']",
            ),
        ],
    )
    def test_calculate_return_name(
        self,
        condition: Condition,
        expected: List[bool],
        data_fix: str,
        request: pytest.FixtureRequest,
    ):
        data: pd.DataFrame = request.getfixturevalue(data_fix)

        result = condition.calculate(data)

        assert result.name == expected


class TestCheckRelation:
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
    def test_calculate_is_string_condition_false_for_none(
        self, condition: Condition, sample_data_with_none
    ):
        expected = [False, False, False]

        result = condition.calculate(sample_data_with_none)
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
    def test_calculate_is_number_condition_false_for_none(
        self, condition: Condition, expected: List[bool], sample_data_with_none
    ):
        result = condition.calculate(sample_data_with_none)
        result = result.tolist()

        assert result == expected
