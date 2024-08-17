from typing import Literal


class OrderResult:
    def __init__(
        self,
        symbol: str,
        place_time: float,
        fill_time: float | None,
        status: Literal["placed", "filled", "cancled", "error"],
    ) -> None:
        pass


class OrderHistory:
    pass
