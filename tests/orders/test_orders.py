from py_trading_lib.orders.orders import *


class TestOrderSpotMarketBuy:
    def test_get_transaction_currency_buy(self):
        order = OrderSpotMarketBuy("USDT/BTC", 100)

        coin = order.get_transaction_currency()

        assert coin == "USDT"

    # def test_backtest(self):
    #     order = OrderSpotMarketBuy("USDT/BTC", 100)
    #     base_cur, quote_cur = order.backtest(ohclv=[0, 0, 50, 0, 0])
    #
    #     assert base_cur.name == "USDT"
    #     assert base_cur.modify_total_amount == -100
    #     assert base_cur.modify_available_amount == -100
    #
    #     assert quote_cur.name == "USDT"
    #     assert quote_cur.modify_total_amount == 2
    #     assert quote_cur.modify_available_amount == 2
    #


class TestOrderSpotMarketSell:
    def test_get_transaction_currency_sell(self):
        order = OrderSpotMarketSell("USDT/BTC", 100)

        coin = order.get_transaction_currency()

        assert coin == "BTC"
