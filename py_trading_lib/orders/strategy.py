from abc import ABC, abstractmethod
from typing import Tuple, List

from py_trading_lib.analysis.analysis import Analysis
from py_trading_lib.orders.orders import Order

__all__ = ["Strategy", "StrategyAlternatingLive", "StrategyAlternatingBacktest"]


class Strategy(ABC):
    def __init__(self, analysis: Analysis) -> None:
        self._analysis = analysis
        self._orders: List[Tuple[str, Order]] = []

    def add_order(self, signal: str, order: Order) -> None:
        self._orders.append((signal, order))

    @abstractmethod
    def execute_orders(self):
        pass


class BacktestingStrategy(Strategy):
    def execute_orders(self):
        raise NotImplementedError

    def _map_orders_to_signals(self):
        raise NotImplementedError


class LiveTradingStrategy(Strategy):
    def execute_orders(self):
        raise NotImplementedError


class StrategyAlternating:
    def _check_max_orders_reached(self, orders: List[Tuple[str, Order]]):
        max_orders = 2
        if len(orders) >= max_orders:
            raise ValueError(
                "In an StrategyAlternating class not more than 2 orders can be added."
            )


class StrategyAlternatingBacktest(BacktestingStrategy, StrategyAlternating):
    def add_order(self, signal: str, order: Order) -> None:
        self._check_max_orders_reached(self._orders)
        return super().add_order(signal, order)


class StrategyAlternatingLive(LiveTradingStrategy, StrategyAlternating):
    def add_order(self, signal: str, order: Order) -> None:
        self._check_max_orders_reached(self._orders)
        return super().add_order(signal, order)
