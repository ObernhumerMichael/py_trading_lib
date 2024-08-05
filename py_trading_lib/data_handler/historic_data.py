import pandas as pd

import py_trading_lib.utils.sanity_checks as sanity

__all__ = ["LocalKlines"]


class LocalKlines:
    def get_tohlcv_from_csv(self, path: str) -> pd.DataFrame:
        self._perform_sanity_checks(path)

        data = self._try_read_data(path)

        self._validate(data)

        return data

    def _perform_sanity_checks(self, path):
        sanity.check_file_exist(path)
        sanity.check_is_file_csv(path)

    def _try_read_data(self, path: str):
        try:
            data = pd.read_csv(path)
        except Exception as e:
            raise RuntimeError(
                f"Something went wrong while reading the data from the file: {path}."
            ) from e

        return data

    def _validate(self, data: pd.DataFrame):
        sanity.check_cols_for_tohlcv(data)
        sanity.check_contains_only_numbers(data)
