from typing import Union, Any, List

import pandas as pd

__all__ = ["convert_to_df_from_sr_or_df", "is_series_or_dataframe"]


def convert_to_df_from_sr_or_df(
    convert: Union[pd.DataFrame, pd.Series, Any]
) -> pd.DataFrame:
    if is_series_or_dataframe(convert):
        return pd.DataFrame(convert)
    else:
        raise TypeError(
            f"The passed variable is neither a DataFrame nor a Series but a {type(convert)}. Thus the variable could not be converted to a DataFrame."
        )


def is_series_or_dataframe(var: Any) -> bool:
    return isinstance(var, pd.DataFrame) or isinstance(var, pd.Series)


def select_only_needed_cols(cols: List[str], df: pd.DataFrame) -> pd.DataFrame:
    selection = df[cols]
    selection = convert_to_df_from_sr_or_df(selection)
    return selection


def type_check_is_series(check: Any) -> pd.Series:
    if isinstance(check, pd.Series):
        return check
    else:
        raise TypeError("The object to check is not a pandas Series.")
