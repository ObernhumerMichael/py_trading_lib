class SystemState:
    def __init__(self) -> None:
        self._total_balance: float | None = None
        self._current_price: float | None = None

    @property
    def total_balance(self) -> float:
        if self._total_balance is None:
            raise ValueError("total_balance has not been defined yet.")
        return self._total_balance

    @total_balance.setter
    def total_balance(self, value: float) -> None:
        if value < 0:
            raise ValueError("total_balance cannot be negative")
        self._total_balance = value

    @property
    def current_price(self) -> float:
        if self._current_price is None:
            raise ValueError("current_price has not been defined yet.")
        return self._current_price

    @current_price.setter
    def current_price(self, value: float) -> None:
        if value < 0:
            raise ValueError("current_price must be greater than zero")
        self._current_price = value

    def is_valid(self) -> bool:
        return self._total_balance is not None and self._current_price is not None
