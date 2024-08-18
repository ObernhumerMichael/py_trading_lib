from typing import Literal


class OrderResult:
    # should also contain how the system has changed
    # amount asset 1 & 2
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
