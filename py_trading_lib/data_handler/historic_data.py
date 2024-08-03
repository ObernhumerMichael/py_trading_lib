import pandas as pd

from ..utils.sanity_checks import *


class LocalKlines:
    def get_tohlcv_from_csv(self, path: str) -> pd.DataFrame:
        self._sanity_checks(path)

        data = self._try_read_data(path)

        self._validate(data)

        return data

    def _sanity_checks(self, path):
        check_file_exist(path)
        check_is_file_csv(path)

    def _try_read_data(self, path: str):
        try:
            data = pd.read_csv(path)
        except Exception as e:
            raise RuntimeError(
                f"Something went wrong while reading the data from the file: {path}."
            ) from e

        return data

    def _validate(self, data: pd.DataFrame):
        check_cols_for_tohlcv(data)
        check_contains_only_numbers(data)
