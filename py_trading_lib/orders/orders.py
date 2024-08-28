from abc import ABC, abstractmethod
from typing import Literal, List, Tuple


from py_trading_lib.orders.coin import ModifyCoin


class Order(ABC):
    @abstractmethod
    def __init__(self, symbol: str, amount: float) -> None:
        self._symbol = symbol
        self._amount = amount
        self._side: Literal["buy", "sell"]

    def is_placeable(self, available: float) -> bool:
        return available >= self._amount

    @abstractmethod
    def get_transaction_currency(self) -> str:
        pass

    @abstractmethod
    def place_on_exchange(self):
        pass

    @abstractmethod
    def backtest(self, ohclv: List[float]) -> Tuple[ModifyCoin, ModifyCoin]:
        pass


class OrderSpotBuy(Order):
    def __init__(self, symbol: str, amount: float) -> None:
        super().__init__(symbol, amount)
        self._side = "buy"

    def get_transaction_currency(self) -> str:
        currency = self._symbol.split("/")
        return currency[0]


class OrderSpotSell(Order):
    def __init__(self, symbol: str, amount: float) -> None:
        super().__init__(symbol, amount)
        self._side = "sell"

    def get_transaction_currency(self) -> str:
        currency = self._symbol.split("/")
        return currency[1]


class OrderSpotMarketBuy(OrderSpotBuy):
    def place_on_exchange(self):
        raise NotImplementedError

    def backtest(self, ohclv: List[float]) -> Tuple[ModifyCoin, ModifyCoin]:
        raise NotImplementedError


class OrderSpotMarketSell(OrderSpotSell):
    def place_on_exchange(self):
        raise NotImplementedError

    def backtest(self, ohclv: List[float]) -> Tuple[ModifyCoin, ModifyCoin]:
        return super().backtest(ohclv)
