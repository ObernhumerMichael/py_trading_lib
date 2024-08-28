from abc import ABC, abstractmethod

from py_trading_lib.system.state import SystemState


class Allocation(ABC):
    @abstractmethod
    def get_order_size(self, system_state: SystemState) -> float:
        pass


class AllocationFixed(Allocation):
    """A fixed amount of cryptocurrency to be traded with each order."""

    def __init__(self, order_size: float) -> None:
        self.order_size = order_size

    def get_order_size(self, system_state: SystemState) -> float:
        return self.order_size


class AllocationIterativePercentage(Allocation):
    """
    This strategy ensures that all available capital is gradually used in multiple trades,
    with each trade being a percentage of the remaining balance.
    """

    def __init__(self, percentage: float, min_order_size: float) -> None:
        self.percentage = percentage
        self.min_order_size = min_order_size

    def get_order_size(self, system_state: SystemState) -> float:
        total_balance = system_state.total_balance
        current_price = system_state.current_price
        raise NotImplementedError


class AllocationFixedNumberOfTrades(Allocation):
    """
    Allow the user to specify the number of trades they want to split their capital into,
    and then calculate each trade size as a percentage of the total balance divided by that number.
    """

    def __init__(self, num_trades: int) -> None:
        self.num_trades = num_trades

    def get_order_size(self, system_state: SystemState, active_trades: int) -> float:
        total_balance = system_state.total_balance
        current_price = system_state.current_price
        raise NotImplementedError
