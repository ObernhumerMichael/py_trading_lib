import pytest

import pandas as pd

from py_trading_lib.orders.orders import *


@pytest.fixture
def order_generator():
    signal = pd.Series([True, False])
    return OrderGenerator(signal, OrderLongOpen())


class TestOrderGenerator:
    def test_open_return_nans(
        self,
        order_generator: OrderGenerator,
    ):
        orders = order_generator.generate()

        order_nans = orders.isna()
        order_nans = order_nans.tolist()
        assert order_nans == [False, True]

    def test_open_return_types(self, order_generator: OrderGenerator):
        expected = pd.Series([OrderLongOpen(), None])

        orders = order_generator.generate()

        order_types = orders.map(type)
        expected_types = expected.map(type)
        pd.testing.assert_series_equal(order_types, expected_types)

    def test_open_return_is_not_reference(
        self,
    ):
        order_generator = OrderGenerator(pd.Series([True, True]), OrderLongOpen())
        orders = order_generator.generate()
        assert orders[0] is not orders[1]
