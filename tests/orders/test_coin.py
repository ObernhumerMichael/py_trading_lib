import pytest

from py_trading_lib.orders.coin import *


@pytest.fixture
def example_portfolio() -> Portfolio:
    portfolio = Portfolio()
    btc = Coin("BTC", 100, 50)

    portfolio.add_coin(btc)

    return portfolio


class TestCoin:
    def test_change_total_by_negative_fail(self):
        btc = Coin("BTC", 100, 50)
        with pytest.raises(ValueError):
            btc.modify_total_by(-1000)

    def test_change_available_by_negative_fail(self):
        btc = Coin("BTC", 100, 50)
        with pytest.raises(ValueError):
            btc.modify_available_by(-100)


class TestPortfolio:
    def test_add_coin_pass(self):
        portfolio = Portfolio()
        btc = Coin("BTC", 100, 50)

        portfolio.add_coin(btc)

        assert portfolio._portfolio["BTC"] == btc

    def test_add_coin_fail(self):
        portfolio = Portfolio()
        btc = Coin("BTC", 100, 50)
        portfolio.add_coin(btc)

        with pytest.raises(KeyError):
            portfolio.add_coin(btc)

    def test_modify_pass(self, example_portfolio: Portfolio):
        btc_modification = ModifyCoin("BTC", modify_total_by=0, modify_available_by=-10)

        example_portfolio.modify_coin(btc_modification)

        btc = example_portfolio._portfolio["BTC"]
        assert btc.get_total() == 100
        assert btc.get_available() == 40

    def test_modify_fail(self, example_portfolio: Portfolio):
        btc_modification = ModifyCoin("ETH", modify_total_by=0, modify_available_by=-10)

        with pytest.raises(KeyError):
            example_portfolio.modify_coin(btc_modification)

    def test_get_total_pass(self, example_portfolio: Portfolio):
        expected_total = 100

        total = example_portfolio.get_total("BTC")

        assert total == expected_total

    def test_get_total_fail(self, example_portfolio: Portfolio):
        with pytest.raises(KeyError):
            example_portfolio.get_total("ETH")

    def test_get_available_pass(self, example_portfolio: Portfolio):
        expected_total = 50

        total = example_portfolio.get_available("BTC")

        assert total == expected_total

    def test_get_available_fail(self, example_portfolio: Portfolio):
        with pytest.raises(KeyError):
            example_portfolio.get_available("ETH")
