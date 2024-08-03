import pandas as pd


def check_cols_for_tohlcv(klines: pd.DataFrame) -> None:
    required_cols = ["TIME", "OPEN", "HIGH", "LOW", "CLOSE", "VOLUME"]
    columns = klines.columns.tolist()
    cols_exist = set(required_cols).issubset(set(columns))

    if not cols_exist:
        raise ValueError(
            f"The following columns must be present in the DataFrame: {required_cols}. Currently only the following are present: {columns}"
        )


def check_has_min_len(df: pd.DataFrame, min_len: int) -> None:
    len_klines = len(df)

    if len_klines < min_len:
        raise ValueError(
            f"The klines have a length of {len_klines} and a min lenght of {min_len} is needed."
        )


def check_not_empty(df: pd.DataFrame) -> None:
    if df.empty:
        raise ValueError(
            "The DataFrame must contain values otherwise it can't be operated on."
        )


def check_contains_only_bools(df: pd.DataFrame) -> None:
    column_types = df.dtypes
    all_bools = column_types.eq(bool).all()

    if not all_bools:
        raise TypeError("The pandas DataFrame contains values other than bool.")
