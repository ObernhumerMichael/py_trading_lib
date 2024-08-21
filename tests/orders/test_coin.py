import pytest

from py_trading_lib.orders.coin import *


class TestCoin:
    def test_change_total_by_negative_fail(self):
        btc = Coin("BTC", 100, 50)
        with pytest.raises(ValueError):
            btc.modify_total_by(-1000)

    def test_change_available_by_negative_fail(self):
        btc = Coin("BTC", 100, 50)
        with pytest.raises(ValueError):
            btc.modify_available_by(-100)


class TestModifyCoin:
    def test_modify_coin_pass(self):
        btc = Coin("BTC", 100, 50)
        modification = ModifyCoin("BTC", -10, -10)

        modification.modify_coin(btc)

        assert btc.get_total() == 90
        assert btc.get_available() == 40

    def test_modify_coin_fail(self):
        btc = Coin("BTC", 100, 50)
        modification = ModifyCoin("BTC", 0, -60)

        with pytest.raises(ValueError):
            modification.modify_coin(btc)
