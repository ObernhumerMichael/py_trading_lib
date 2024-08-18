import pytest

import pandas as pd

from py_trading_lib.analysis import *
from py_trading_lib.orders.strategy import *
from py_trading_lib.orders.orders import *
from py_trading_lib.orders.strategy import BacktestingStrategy


@pytest.fixture
def example_analysis():
    analysis = Analysis()

    sma = analysis.add_ti(SMA(2))[0]
    analysis.add_condition(CheckRelation(sma, ">", 5))
    analysis.add_condition(CheckRelation(sma, "<", 5))

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
def example_analysis_data():
    analysis_data_raw = {
        "SMA_2>5": [False, False, True],
        "SMA_2<5": [True, False, False],
    }
    example_analysis_data = pd.DataFrame(analysis_data_raw)
    return example_analysis_data


@pytest.fixture
def example_buy_order():
    return OrderSpotMarket("BTC/USDT", 1000, "buy")


@pytest.fixture
def example_sell_order():
    return OrderSpotMarket("USDT/BTC", 1000, "sell")


@pytest.fixture
def strategy_alternating_backtest(
    example_analysis: Analysis, example_buy_order: Order, example_sell_order: Order
):
    buy_cond = example_analysis._conditions[0].get_name()
    sell_cond = example_analysis._conditions[1].get_name()

    strategy = StrategyAlternatingBacktest(example_analysis)
    strategy.add_order(buy_cond, example_buy_order)
    strategy.add_order(sell_cond, example_sell_order)

    return strategy


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
    @pytest.mark.parametrize("strategy_fix", ["strategy_alternating_backtest"])
    def test_map_orders_to_signals_return_nans(
        self,
        strategy_fix: str,
        example_analysis_data: pd.DataFrame,
        request: pytest.FixtureRequest,
    ):
        strategy: BacktestingStrategy = request.getfixturevalue(strategy_fix)
        expected_data = {
            "SMA_2>5|BTC/USDT(buy)": [False, False, True],
            "SMA_2<5|USDT/BTC(sell)": [True, False, False],
        }
        expected_nans = pd.DataFrame(expected_data)

        mapped_orders = strategy._map_orders_to_signals(example_analysis_data)
        is_mapped_orders_nan = mapped_orders.notna()

        pd.testing.assert_frame_equal(is_mapped_orders_nan, expected_nans)

    @pytest.mark.parametrize("strategy_fix", ["strategy_alternating_backtest"])
    def test_map_orders_to_signals_types(
        self,
        strategy_fix: str,
        example_analysis_data: pd.DataFrame,
        example_buy_order: Order,
        example_sell_order: Order,
        request: pytest.FixtureRequest,
    ):
        strategy: BacktestingStrategy = request.getfixturevalue(strategy_fix)
        expected_data = {
            "SMA_2>5|BTC/USDT(buy)": [None, None, example_buy_order],
            "SMA_2<5|USDT/BTC(sell)": [example_sell_order, None, None],
        }
        expected_types = pd.DataFrame(expected_data)
        expected_types = expected_types.map(type)

        mapped_orders = strategy._map_orders_to_signals(example_analysis_data)
        mapped_types = mapped_orders.map(type)

        pd.testing.assert_frame_equal(mapped_types, expected_types)


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
                strategy.add_order("TEST", example_buy_order)
