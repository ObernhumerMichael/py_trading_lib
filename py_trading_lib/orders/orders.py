from abc import ABC
from copy import deepcopy

import pandas as pd

__all__ = ["Order", "OrderLongOpen", "OrderLongClose", "OrderGenerator"]


class Order(ABC):
    pass


class OrderLongOpen(Order):
    pass


class OrderLongClose(Order):
    pass


class OrderGenerator:
    def __init__(
        self,
        signal: pd.Series,
        order: Order,
    ) -> None:
        self._signal = signal
        self._order = order

    def generate(self) -> pd.Series:
        positions = self._signal.apply(lambda x: deepcopy(self._order) if x else None)

        if isinstance(positions, pd.Series):
            return positions
        else:
            raise TypeError(
                "Something went wrong during the calculation of the positions."
            )
