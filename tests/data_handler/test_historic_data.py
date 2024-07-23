import pytest
import pandas as pd

from py_trading_lib.data_handler.historic_data import KlineChecks, LocalKlines


class TestLocalKlines:
    def test_get_from_csv_len(self):
        valid_file_len = 8640

        klines = LocalKlines().get_from_csv("./example_klines/BTC_USDT.csv")

        assert len(klines) == valid_file_len

    def test_get_from_csv_columns(self):
        expected_columns = ["TIME", "OPEN", "HIGH", "LOW", "CLOSE", "VOLUME"]
        klines = LocalKlines().get_from_csv("./example_klines/BTC_USDT.csv")

        columns = klines.columns.tolist()

        assert columns == expected_columns

    def test_get_from_csv_no_file(self):
        with pytest.raises(FileNotFoundError):
            LocalKlines().get_from_csv("./no_file.csv")

    def test_get_from_csv_wrong_file_ending(self):
        with pytest.raises(ValueError):
            LocalKlines().get_from_csv("./tests/data_handler/wrong-file.txt")

    def test_get_from_csv_wrong_format(self):
        with pytest.raises(ValueError):
            LocalKlines().get_from_csv("./tests/data_handler/wrong-format.csv")


class TestKlineChecks:
    def test_check_columns_fail(self, not_kline_data: pd.DataFrame):
        with pytest.raises(ValueError):
            KlineChecks().check_columns(not_kline_data)

    def test_check_columns_pass(self, example_klines):
        KlineChecks().check_columns(example_klines)

    def test_check_has_min_len_fail(self, insufficient_klines: pd.DataFrame):
        min_len = 10

        with pytest.raises(ValueError):
            KlineChecks().check_has_min_len(insufficient_klines, min_len)

    def test_check_has_min_len_pass(self, example_klines: pd.DataFrame):
        min_len = 10
        KlineChecks().check_has_min_len(example_klines, min_len)
