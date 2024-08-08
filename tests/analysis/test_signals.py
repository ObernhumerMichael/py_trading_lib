from typing import List

import pytest
import pandas as pd

from py_trading_lib.analysis.signals import *


@pytest.fixture
def sample_conditions():
    conditions = {
        "a": [True, True, False],
        "b": [True, False, False],
        "c": [True, False, False],
    }
    return pd.DataFrame(conditions)


@pytest.fixture
def sample_broken_condition():
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
        "z": [False, False, False],
    }
    return pd.DataFrame(conditions)


@pytest.fixture
def signal_all_conditions_true():
    return SignalAllConditionsTrue(["a", "b", "c"])


class TestSignals:
    @pytest.mark.parametrize("signal", [SignalAllConditionsTrue(["a"])])
    def test_calculate_signal_empty_conditions(self, signal: Signal):
        with pytest.raises(ValueError):
            signal.calculate_signal(pd.DataFrame())

    @pytest.mark.parametrize("signal", [SignalAllConditionsTrue(["z"])])
    def test_calculate_signal_incomplete_data(
        self, signal: Signal, sample_conditions: pd.DataFrame
    ):
        with pytest.raises(ValueError):
            signal.calculate_signal(sample_conditions)

    @pytest.mark.parametrize(
        "signal_fix, expected",
        [("signal_all_conditions_true", [True, False, False])],
    )
    def test_calculate_signal_valid_conditions(
        self,
        signal_fix: str,
        sample_conditions: pd.DataFrame,
        expected: List[bool],
        request: pytest.FixtureRequest,
    ):
        signal = request.getfixturevalue(signal_fix)

        result = signal.calculate_signal(sample_conditions)
        result = result.tolist()

        assert result == expected

    @pytest.mark.parametrize(
        "signal_fix",
        ["signal_all_conditions_true"],
    )
    def test_calculate_signal_invalid_conditions(
        self,
        signal_fix: str,
        sample_broken_condition: pd.DataFrame,
        request: pytest.FixtureRequest,
    ):
        signal = request.getfixturevalue(signal_fix)

        with pytest.raises(TypeError):
            signal.calculate_signal(sample_broken_condition)

    @pytest.mark.parametrize(
        "signal_fix, expected",
        [("signal_all_conditions_true", [True, True, True])],
    )
    def test_calculate_signal_only_expected_cols(
        self,
        signal_fix: str,
        expected: List[bool],
        sample_extended_conditions: pd.DataFrame,
        request: pytest.FixtureRequest,
    ):
        signal = request.getfixturevalue(signal_fix)

        result = signal.calculate_signal(sample_extended_conditions)
        result = result.tolist()

        assert result == expected
