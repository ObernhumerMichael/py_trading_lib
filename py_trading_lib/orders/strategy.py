from abc import ABC, abstractmethod
from typing import Tuple, List, Union

import pandas as pd

from py_trading_lib.analysis.analysis import Analysis
from py_trading_lib.orders.orders import Order
import py_trading_lib.utils.utils as utils

__all__ = ["Strategy", "StrategyAlternatingLive", "StrategyAlternatingBacktest"]


class Strategy(ABC):
    def __init__(self, analysis: Analysis) -> None:
        self._analysis = analysis
        self._orders: List[Tuple[str, Order]] = []

    def add_order(self, signal: str, order: Order) -> None:
        self._orders.append((signal, order))

    @abstractmethod
    def execute_orders(self):
        pass

    @abstractmethod
    def _perform_sanity_checks(self):
        pass


class BacktestingStrategy(Strategy):
    def execute_orders(self):
        raise NotImplementedError

    def _perform_sanity_checks(self):
        raise NotImplementedError

    def _map_orders_to_signals(self, analysis_data: pd.DataFrame) -> pd.DataFrame:
        mapp = {}
        signals: List[str] = []
        for signal, order in self._orders:
            replace = {False: None, True: order}
            mapp[signal] = replace
            signals.append(signal)

        data_to_map = analysis_data[signals]
        data_to_map = utils.convert_to_df_from_sr_or_df(data_to_map)

        mapped_orders = data_to_map.replace(mapp)

        for signal, order in self._orders:
            mapped_orders.rename(
                columns={signal: f"{signal}|{order._symbol}({order._side})"},
                inplace=True,
            )

        return mapped_orders

    def _linearize_mapped_orders(self, mapped_orders: pd.DataFrame) -> pd.Series:
        linearized_raw: List[Union[None, Order]] = []
        for _, row in mapped_orders.iterrows():
            linearized_raw.extend(row.tolist())
        linearized = pd.Series(linearized_raw, name="linearized_orders")
        return linearized


class LiveTradingStrategy(Strategy):
    def execute_orders(self):
        raise NotImplementedError

    def _perform_sanity_checks(self):
        raise NotImplementedError


class StrategyAlternating:
    def _check_max_orders_reached(self, orders: List[Tuple[str, Order]]):
        max_orders = 2
        if len(orders) >= max_orders:
            raise ValueError(
                "In an StrategyAlternating class not more than 2 orders can be added."
            )


class StrategyAlternatingBacktest(BacktestingStrategy, StrategyAlternating):
    def add_order(self, signal: str, order: Order) -> None:
        self._check_max_orders_reached(self._orders)
        return super().add_order(signal, order)


class StrategyAlternatingLive(LiveTradingStrategy, StrategyAlternating):
    def add_order(self, signal: str, order: Order) -> None:
        self._check_max_orders_reached(self._orders)
        return super().add_order(signal, order)
