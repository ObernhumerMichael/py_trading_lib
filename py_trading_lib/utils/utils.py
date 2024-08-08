from typing import Union, Any

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
