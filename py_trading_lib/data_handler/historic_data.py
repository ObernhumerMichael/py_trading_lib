import os

import pandas as pd


class HistoricData:
    def get_from_csv(self, path: str) -> pd.DataFrame:
        self._file_sanity_checks(path)

        data = self._try_read_data(path)

        self._check_columns(data)

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

    def _check_columns(self, data: pd.DataFrame):
        expected_columns = ["TIME", "OPEN", "HIGH", "LOW", "CLOSE", "VOLUME"]

        if expected_columns != data.columns.tolist():
            raise ValueError(
                f"The file does not exist in the following format: {expected_columns}"
            )
