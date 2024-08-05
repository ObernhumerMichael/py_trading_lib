import pytest

from py_trading_lib.data_handler.historic_data import *


class TestLocalKlines:
    def test_get_tohlcv_from_csv_len(self):
        valid_file_len = 8640

        klines = LocalKlines().get_tohlcv_from_csv("./example_klines/BTC_USDT.csv")

        assert len(klines) == valid_file_len

    def test_get_tohlcv_from_csv_columns(self):
        expected_columns = ["TIME", "OPEN", "HIGH", "LOW", "CLOSE", "VOLUME"]
        klines = LocalKlines().get_tohlcv_from_csv("./example_klines/BTC_USDT.csv")

        columns = klines.columns.tolist()

        assert columns == expected_columns

    def test_get_tohlcv_from_csv_no_file(self):
        with pytest.raises(FileNotFoundError):
            LocalKlines().get_tohlcv_from_csv("./no_file.csv")

    def test_get_tohlcv_from_csv_wrong_file_ending(self):
        with pytest.raises(ValueError):
            LocalKlines().get_tohlcv_from_csv("./tests/data_handler/wrong_file.txt")

    def test_get_tohlcv_from_csv_wrong_format(self):
        with pytest.raises(ValueError):
            LocalKlines().get_tohlcv_from_csv("./tests/data_handler/wrong_format.csv")

    def test_get_tohlcv_from_csv_missing_data(self):
        with pytest.raises(ValueError):
            LocalKlines().get_tohlcv_from_csv("./tests/data_handler/missing_data.csv")

    def test_get_tohlcv_from_csv_broken_data(self):
        with pytest.raises(TypeError):
            LocalKlines().get_tohlcv_from_csv("./tests/data_handler/broken_data.csv")
