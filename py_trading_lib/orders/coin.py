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


class ModifyCoin:
    def __init__(
        self, name: str, modify_total_by: float, modify_available_by: float
    ) -> None:
        self.__name = name
        self.__modify_total_amount = modify_total_by
        self.__modify_available_amount = modify_available_by

    def modify_coin(self, coin: Coin):
        coin.modify_total_by(self.__modify_total_amount)
        coin.modify_available_by(self.__modify_available_amount)

    def get_name(self) -> str:
        return self.__name
