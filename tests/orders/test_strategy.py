import pytest

import pandas as pd

from py_trading_lib.analysis import *
from py_trading_lib.orders.strategy import *
from py_trading_lib.orders.orders import *


@pytest.fixture
def example_analysis():
    analysis = Analysis()

    sma = analysis.add_ti(SMA(2))[0]
    check_relation = analysis.add_condition(CheckRelation(sma, ">", 2))
    analysis.add_condition(CheckAllTrue([check_relation]))

    return analysis


@pytest.fixture
def example_tohclv():
    tohclv = {
        "TIME": [1679144400000, 1679148000000, 1679151600000, 1679155200000],
        "OPEN": [1, 1, 1, 1],
        "HIGH": [1, 1, 1, 1],
        "LOW": [1, 1, 1, 1],
        "CLOSE": [1, 1, 10, 10],
        "VOLUME": [1, 1, 1, 1],
    }
    return pd.DataFrame(tohclv)


@pytest.fixture
def strategy_alternating_backtest(example_analysis: Analysis):
    strategy = StrategyAlternatingBacktest(example_analysis)
    return strategy


@pytest.fixture
def example_buy_order():
    return OrderSpotMarket("BTC/USDT", 1000, "buy")


class TestAllStrategy:
    @pytest.mark.parametrize(
        "strategy",
        [
            StrategyAlternatingBacktest(Analysis()),
            StrategyAlternatingLive(Analysis()),
        ],
    )
    def test_add_order_pass(self, strategy: Strategy, example_buy_order: Order):
        strategy.add_order("CheckAllTrue=['SMA_2>2']", example_buy_order)

        assert len(strategy._orders) == 1


class TestBacktestingStrategy:
    pass


class TestStrategyAlternatingSpecific:
    @pytest.mark.parametrize(
        "strategy",
        [
            StrategyAlternatingBacktest(Analysis()),
            StrategyAlternatingLive(Analysis()),
        ],
    )
    def test_add_order_too_many_signals(self, strategy: Strategy, example_buy_order):

        with pytest.raises(ValueError):
            for _ in range(3):
                strategy.add_order("CheckAllTrue=['SMA_2>2']", example_buy_order)
