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

    @pytest.mark.parametrize("signal", ["signal_all_conditions_true_valid_conditions"])
    def test_sanity_check_pass(self, signal: ISignal, request):
        signal = request.getfixturevalue(signal)

        signal._sanity_checks()

    @pytest.mark.parametrize("signal", ["signal_all_conditions_true_broken_conditions"])
    def test_sanity_check_fail(self, signal: ISignal, request):
        signal = request.getfixturevalue(signal)

        with pytest.raises(ValueError):
            signal._sanity_checks()

    @pytest.mark.parametrize("signal", [SignalAllConditionsTrue(pd.DataFrame())])
    def test_is_signal_true_empty_conditions(self, signal: ISignal):
        with pytest.raises(ValueError):
            signal.is_signal_true()

    @pytest.mark.parametrize(
        "signal, expected",
        [
            ("signal_all_conditions_true_valid_conditions", [True, False, False]),
        ],
    )
    def test_is_signal_true_valid_conditions(
        self, signal: ISignal, expected: List[bool], request
    ):
        signal = request.getfixturevalue(signal)

        result = signal.is_signal_true()
        result = result.tolist()

        assert result == expected

    @pytest.mark.parametrize(
        "signal",
        ["signal_all_conditions_true_broken_conditions"],
    )
    def test_is_signal_true_invalid_conditions(self, signal: ISignal, request):
        signal = request.getfixturevalue(signal)

        with pytest.raises(ValueError):
            signal.is_signal_true()
