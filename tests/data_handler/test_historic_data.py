import pytest

from py_trading_lib.data_handler.historic_data import HistoricData


class TestHistoricData:

    def test_get_from_csv_len(self):
        valid_file_len = 8640

        klines = HistoricData().get_from_csv("./example_klines/BTC_USDT.csv")

        assert len(klines) == valid_file_len

    def test_get_from_csv_columns(self):
        expected_columns = ["TIME", "OPEN", "HIGH", "LOW", "CLOSE", "VOLUME"]
        klines = HistoricData().get_from_csv("./example_klines/BTC_USDT.csv")

        columns = klines.columns.tolist()

        assert columns == expected_columns

    def test_get_from_csv_no_file(self):
        with pytest.raises(FileNotFoundError):
            HistoricData().get_from_csv("./no_file.csv")

    def test_get_from_csv_wrong_file_ending(self):
        with pytest.raises(ValueError):
            HistoricData().get_from_csv("./tests/data_handler/wrong-file.txt")

    def test_get_from_csv_wrong_format(self):
        with pytest.raises(ValueError):
            HistoricData().get_from_csv("./tests/data_handler/wrong-format.csv")
