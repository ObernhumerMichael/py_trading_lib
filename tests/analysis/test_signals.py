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
def signal_all_conditions_true_valid_conditions(sample_conditions):
    return SignalAllConditionsTrue(sample_conditions)


@pytest.fixture
def signal_all_conditions_true_broken_conditions(sample_broken_condition):
    return SignalAllConditionsTrue(sample_broken_condition)


class TestSignals:
    @pytest.mark.parametrize("signal", [SignalAllConditionsTrue(pd.DataFrame())])
    def test_calculate_signal_empty_conditions(self, signal: Signal):
        with pytest.raises(ValueError):
            signal.calculate_signal()

    @pytest.mark.parametrize(
        "signal, expected",
        [
            ("signal_all_conditions_true_valid_conditions", [True, False, False]),
        ],
    )
    def test_calculate_signal_valid_conditions(
        self, signal: Signal, expected: List[bool], request
    ):
        signal = request.getfixturevalue(signal)

        result = signal.calculate_signal()
        result = result.tolist()

        assert result == expected

    @pytest.mark.parametrize(
        "signal",
        ["signal_all_conditions_true_broken_conditions"],
    )
    def test_calculate_signal_invalid_conditions(self, signal: Signal, request):
        signal = request.getfixturevalue(signal)

        with pytest.raises(TypeError):
            signal.calculate_signal()
