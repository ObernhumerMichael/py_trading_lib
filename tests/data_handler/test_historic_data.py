import pytest

from py_trading_lib.data_handler.historic_data import HistoricData


class TestHistoricData:
    def __init__(self) -> None:
        self.historic_data = HistoricData()

    def test_get_data_from_file_len(self):
        valid_file_len = 8640

        klines = self.historic_data.get_data_from_file(
            "../../example_klines/BTC_USDT.csv"
        )

        assert len(klines) == valid_file_len

    def test_get_data_from_file_columns(self):
        expected_columns = ["TIME", "OPEN", "HIGH", "LOW", "CLOSE", "VOLUME"]
        klines = self.historic_data.get_data_from_file(
            "../../example_klines/BTC_USDT.csv"
        )

        columns = klines.columns.tolist()

        assert columns == expected_columns

    def test_get_data_from_file_no_file(self):
        with pytest.raises(FileNotFoundError):
            self.historic_data.get_data_from_file("no_file.csv")

    def test_get_data_from_file_wrong_format(self):
        with pytest.raises(ValueError):
            self.historic_data.get_data_from_file("./wrong-file.csv")
