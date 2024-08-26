import pytest

import pandas as pd

from py_trading_lib.analysis import *
from py_trading_lib.orders.strategy import *
from py_trading_lib.orders.orders import *
from py_trading_lib.orders.strategy import BacktestingStrategy


@pytest.fixture
def example_analysis() -> Analysis:
    analysis = Analysis()

    sma = analysis.add_ti(SMA(2))[0]
    analysis.add_condition(CheckRelation(sma, ">", 5))
    analysis.add_condition(CheckRelation(sma, "<", 5))

    return analysis


@pytest.fixture
def example_buy_order() -> Order:
    return OrderSpotMarketBuy("BTC/USDT", 1000)


@pytest.fixture
def example_sell_order() -> Order:
    return OrderSpotMarketSell("USDT/BTC", 1000)


@pytest.fixture
def strategy_alternating_backtest(
    example_analysis: Analysis, example_buy_order: Order, example_sell_order: Order
) -> Strategy:
    buy_cond = example_analysis._conditions[0].get_name()
    sell_cond = example_analysis._conditions[1].get_name()

    strategy = StrategyAlternatingBacktest()
    strategy.add_order(buy_cond, example_buy_order)
    strategy.add_order(sell_cond, example_sell_order)

    return strategy


class TestAllStrategy:
    @pytest.mark.parametrize(
        "strategy",
        [
            StrategyAlternatingBacktest(),
            StrategyAlternatingLive(),
        ],
    )
    def test_add_order_pass(self, strategy: Strategy, example_buy_order: Order):
        strategy.add_order("CheckAllTrue=['SMA_2>2']", example_buy_order)

        assert len(strategy._orders) == 1


@pytest.fixture
def example_analysis_data() -> pd.DataFrame:
    analysis_data_raw = {
        "SMA_2>5": [False, False, True],
        "SMA_2<5": [True, False, False],
    }
    example_analysis_data = pd.DataFrame(analysis_data_raw)
    return example_analysis_data


@pytest.fixture
def example_mapped_orders(
    example_buy_order: Order, example_sell_order: Order
) -> pd.DataFrame:
    mapped_orders_data = {
        "SMA_2>5|BTC/USDT(buy)": [
            None,
            None,
            example_buy_order,
            example_buy_order,
            example_buy_order,
        ],
        "SMA_2<5|USDT/BTC(sell)": [
            None,
            example_sell_order,
            None,
            example_sell_order,
            example_sell_order,
        ],
    }
    mapped_orders = pd.DataFrame(mapped_orders_data)
    return mapped_orders


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

    @pytest.mark.parametrize("strategy_fix", ["strategy_alternating_backtest"])
    def test_map_orders_to_signals_result(
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
        expected = pd.DataFrame(expected_data)

        mapped_orders = strategy._map_orders_to_signals(example_analysis_data)

        pd.testing.assert_frame_equal(mapped_orders, expected)

    def test_serialize_mapped_orders(
        self,
        strategy_alternating_backtest: BacktestingStrategy,
        example_mapped_orders: pd.DataFrame,
        example_buy_order: Order,
        example_sell_order: Order,
    ):
        expected = pd.Series(
            [
                None,  # order 1
                None,  # order 2
                None,  # order 1
                example_sell_order,  # order 2
                example_buy_order,  # order 1
                None,  # order 2
                example_buy_order,  # order 1
                example_sell_order,  # order 2
                example_buy_order,  # order 1
                example_sell_order,  # order 2
            ],
            name="linearized_orders",
        )

        linearized_orders = strategy_alternating_backtest._serialize_mapped_orders(
            example_mapped_orders
        )

        pd.testing.assert_series_equal(linearized_orders, expected)


class TestStrategyAlternatingSpecific:
    @pytest.mark.parametrize(
        "strategy",
        [
            StrategyAlternatingBacktest(),
            StrategyAlternatingLive(),
        ],
    )
    def test_add_order_too_many_signals(self, strategy: Strategy, example_buy_order):

        with pytest.raises(ValueError):
            for _ in range(3):
                strategy.add_order("TEST", example_buy_order)
