from typing import List

import pytest
import pandas as pd

from py_trading_lib.analysis.signals import ISignal, SignalAllConditionsTrue


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
        "a": [None, False, None],
        "b": [True, None, None],
        "c": [True, False, None],
    }
    return pd.DataFrame(conditions)


@pytest.fixture
def sample_mixed_condition():
    conditions = {
        "a": [True, True, False, None, False, None],
        "b": [True, False, False, True, None, None],
        "c": [True, False, False, True, False, None],
    }
    return pd.DataFrame(conditions)


@pytest.fixture
def signal_all_conditions_true_valid_conditions(sample_conditions):
    return SignalAllConditionsTrue(sample_conditions)


@pytest.fixture
def signal_all_conditions_true_broken_conditions(sample_broken_condition):
    return SignalAllConditionsTrue(sample_broken_condition)


@pytest.fixture
def signal_all_conditions_true_mixed_conditions(sample_mixed_condition):
    return SignalAllConditionsTrue(sample_mixed_condition)


class TestSignals:

    @pytest.mark.parametrize("signal", [SignalAllConditionsTrue(pd.DataFrame())])
    def test_is_signal_true_empty_conditions(self, signal: ISignal):
        with pytest.raises(ValueError):
            signal.is_signal_true()

    @pytest.mark.parametrize(
        "signal, expected",
        [
            ("signal_all_conditions_true_valid_conditions", [True, False, False]),
            ("signal_all_conditions_true_broken_conditions", [False, False, False]),
            (
                "signal_all_conditions_true_mixed_conditions",
                [True, False, False, False, False, False],
            ),
        ],
    )
    def test_is_signal_true(self, signal: ISignal, expected: List[bool], request):
        signal = request.getfixturevalue(signal)

        result = signal.is_signal_true()
        result = result.tolist()

        assert result == expected
