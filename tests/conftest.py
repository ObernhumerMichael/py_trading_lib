import random

import pytest
import pandas as pd

from py_trading_lib.data_handler.historic_data import LocalKlines


@pytest.fixture
def example_klines():
    klines = LocalKlines().get_tohlcv_from_csv("./example_klines/BTC_USDT.csv")

    klines = klines.tail(400)
    klines = klines.reset_index(drop=True)

    return klines


@pytest.fixture
def insufficient_klines() -> pd.DataFrame:
    kline = {
        "TIME": [1],
        "OPEN": [1],
        "HIGH": [1],
        "LOW": [1],
        "CLOSE": [1],
        "VOLUME": [1],
    }
    return pd.DataFrame(kline)


@pytest.fixture
def not_kline_data() -> pd.DataFrame:
    random_numbers = [random.randint(1, 1000) for _ in range(100)]
    not_kline_data = pd.DataFrame({"TEST": random_numbers})
    return not_kline_data
