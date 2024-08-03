import os

import pandas as pd

from ..utils.sanity_checks import check_cols_for_tohlcv, check_contains_only_numbers


class LocalKlines:
    def get_from_csv(self, path: str) -> pd.DataFrame:
        self._file_sanity_checks(path)

        data = self._try_read_data(path)

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
            data = self._read_data(path)
        except Exception as e:
            raise RuntimeError(
                f"Something went wrong while reading the the data from the file {path}."
            ) from e

        self._check_valid(data)

        return data

    def _check_valid(self, data: pd.DataFrame):
        check_cols_for_tohlcv(data)
        check_contains_only_numbers(data)

    def _read_data(self, path: str):
        return pd.read_csv(path)
