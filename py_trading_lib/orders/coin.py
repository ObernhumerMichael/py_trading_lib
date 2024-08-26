from typing import Dict


class ModifyCoin:
    def __init__(
        self, name: str, modify_total_by: float, modify_available_by: float
    ) -> None:
        self.name = name
        self.modify_total_amount = modify_total_by
        self.modify_available_amount = modify_available_by


class Coin:
    def __init__(self, name: str, total: float, available: float) -> None:
        self.__name = name
        self.__total = total
        self.__available = available

    def modify_total_by(self, amount: float) -> None:
        if amount < 0 and abs(amount) > self.__total:
            raise ValueError("Total cannot be reduced below zero.")
        self.__total += amount

    def modify_available_by(self, amount: float) -> None:
        if amount < 0 and abs(amount) > self.__available:
            raise ValueError("Available cannot be reduced below zero.")
        self.__available += amount

    def get_name(self) -> str:
        return self.__name

    def get_total(self) -> float:
        return self.__total

    def get_available(self) -> float:
        return self.__available

    def __repr__(self) -> str:
        return f"Coin(name={self.__name}, total={self.__total}, available={self.__available})"


class Portfolio:
    def __init__(self) -> None:
        self._portfolio: Dict[str, Coin] = {}

    def add_coin(self, coin: Coin) -> None:
        if self._is_coin_in_portfolio(coin):
            raise KeyError(
                f"The coin: {coin.get_name()} already exists in the portfolio."
            )
        self._portfolio[coin.get_name()] = coin

    def _is_coin_in_portfolio(self, coin: Coin | str) -> bool:
        if isinstance(coin, Coin):
            return coin.get_name() in self._portfolio
        if isinstance(coin, str):
            return coin in self._portfolio

    def modify_coin(self, modification: ModifyCoin) -> None:
        self._check_coin_in_portfolio(modification.name)

        coin = self._portfolio[modification.name]
        coin.modify_total_by(modification.modify_total_amount)
        coin.modify_available_by(modification.modify_available_amount)

    def get_total(self, coin: str) -> float:
        self._check_coin_in_portfolio(coin)
        return self._portfolio[coin].get_total()

    def get_available(self, coin: str) -> float:
        self._check_coin_in_portfolio(coin)
        return self._portfolio[coin].get_available()

    def _check_coin_in_portfolio(self, coin: Coin | str):
        if not self._is_coin_in_portfolio(coin):
            raise KeyError(f"The coin: {coin} is not in the portfolio.")
