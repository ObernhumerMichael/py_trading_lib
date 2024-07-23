from py_trading_lib.analysis.technical_indicators import SMA
from py_trading_lib.data_handler.historic_data import LocalKlines


klines = LocalKlines().get_from_csv("./example_klines/BTC_USDT.csv")
klines = klines.tail(400).reset_index(drop=True)

sma = SMA(5)
indicator = sma.calculate(klines)

print(indicator.head(10).to_dict())
