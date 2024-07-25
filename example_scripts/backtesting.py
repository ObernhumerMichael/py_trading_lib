from py_trading_lib.analysis.technical_indicators import RSI
from py_trading_lib.data_handler.historic_data import LocalKlines


klines = LocalKlines().get_from_csv("./example_klines/BTC_USDT.csv")
klines = klines.tail(400).reset_index(drop=True)

sma = RSI(length=5)
indicator = sma.calculate(klines)

print(indicator.tail(10).to_dict())
