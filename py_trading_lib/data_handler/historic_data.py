import os

import pandas as pd


class LocalKlines:
    def get_from_csv(self, path: str) -> pd.DataFrame:
        self._file_sanity_checks(path)

        data = self._try_read_data(path)

        KlineChecks().check_columns(data)

        return data

    def _file_sanity_checks(self, path):
        self._does_file_exist(path)
        self._is_file_csv(path)

    def _does_file_exist(self, path: str):
        if not os.path.exists(path):
            raise FileNotFoundError(f"The file on the path: {path} does not exist.")

    def _is_file_csv(self, path: str):
        if not path.endswith(".csv"):
            raise ValueError(f"The file one {path} is not a CSV file.")

    def _try_read_data(self, path: str):
        try:
            return self._read_data(path)
        except Exception as e:
            raise e

    def _read_data(self, path: str):
        return pd.read_csv(path)


class KlineChecks:
    def check_columns(self, klines: pd.DataFrame):
        expected_columns = ["TIME", "OPEN", "HIGH", "LOW", "CLOSE", "VOLUME"]
        columns = klines.columns.tolist()

        if expected_columns != columns:
            raise ValueError(f"The following columns are needed: {expected_columns}")

    def check_has_min_len(self, klines: pd.DataFrame, min_len: int):
        len_klines = len(klines)

        if len_klines < min_len:
            raise ValueError(
                f"The klines have a length of {len_klines} and a min lenght of {min_len} is needed."
            )
