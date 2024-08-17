from abc import ABC, abstractmethod

from py_trading_lib.analysis.analysis import Analysis
from py_trading_lib.orders.orders import Order


class Strategy(ABC):
    """
    should handle the overal strategy execution
    backtest the orders
    place on exchange
    update the system status
    """

    @abstractmethod
    def __init__(self, analysis: Analysis) -> None:
        self._analysis = analysis

    @abstractmethod
    def add_order(self, signal: str, order: Order):
        raise NotImplementedError

    @abstractmethod
    def place_on_exchange(self):
        raise NotImplementedError

    @abstractmethod
    def backtest(self):
        raise NotImplementedError


class StrategyAlternating(Strategy):
    pass
