from abc import ABC, abstractmethod
from typing import Literal


class Order(ABC):
    @abstractmethod
    def __init__(
        self, symbol: str, amount: float, side: Literal["buy", "sell"]
    ) -> None:
        self._symbol = symbol
        self._amount = amount
        self._side = side

    @abstractmethod
    def place_on_exchange(self, exchange):
        raise NotImplementedError

    @abstractmethod
    def backtest(self):
        raise NotImplementedError


class OrderSpot(Order):
    pass


class OrderSpotMarket(OrderSpot):
    pass
