from abc import ABC, abstractmethod
from typing import Any, List

import pandas as pd
import pandas_ta as ta

from ..utils.sanity_checks import check_cols_for_tohlcv, check_has_min_len


class TechnicalIndicator(ABC):
    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def get_min_len(self) -> int:
        pass

    @abstractmethod
    def get_indicator_names(self) -> List[str]:
        pass

    @abstractmethod
    def _calculate_indicator(self, klines: pd.DataFrame) -> Any:
        pass

    def calculate(self, klines: pd.DataFrame) -> pd.DataFrame:
        self._sanity_checks(klines)
        indicator = self._try_calculate(klines)
        return indicator

    def _sanity_checks(self, klines: pd.DataFrame):
        min_len = self.get_min_len()
        check_cols_for_tohlcv(klines)
        check_has_min_len(klines, min_len)

    def _try_calculate(self, klines: pd.DataFrame) -> pd.DataFrame:
        try:
            indicator = self._calculate_indicator(klines)
        except Exception as e:
            raise e

        indicator = self._convert_to_dataframe(indicator)

        return indicator

    def _convert_to_dataframe(self, indicator: Any) -> pd.DataFrame:
        if isinstance(indicator, pd.DataFrame):
            return indicator
        elif isinstance(indicator, pd.Series):
            return indicator.to_frame()
        else:
            raise TypeError(
                f"Something went wrong during the calculation of the indicator/s: {self.get_indicator_names()}. They are neither a pandas DataFrame nor a pandas Series."
            )


class SMA(TechnicalIndicator):
    def __init__(self, length: int, offset: int = 0) -> None:
        self.length = length
        self.offset = offset

    def _calculate_indicator(self, klines: pd.DataFrame) -> Any:
        sma = ta.sma(
            close=klines["CLOSE"],
            length=self.length,
            offset=self.offset,
        )
        return sma

    def get_min_len(self) -> int:
        return self.length

    def get_indicator_names(self) -> List[str]:
        """
        Example return: ["SMA_5"]
        """
        return [f"SMA_{self.length}"]


class RSI(TechnicalIndicator):
    def __init__(
        self, length: int = 14, scalar: float = 100, drift: int = 1, offset: int = 0
    ) -> None:
        self.length = length
        self.scalar = scalar
        self.drift = drift
        self.offset = offset

    def _calculate_indicator(self, klines: pd.DataFrame) -> Any:
        rsi = ta.rsi(
            close=klines["CLOSE"],
            length=self.length,
            scalar=self.scalar,
            drift=self.drift,
            offset=self.offset,
        )
        return rsi

    def get_min_len(self) -> int:
        return self.length

    def get_indicator_names(self) -> List[str]:
        """
        Example return: ["RSI_5"]
        """
        return [f"RSI_{self.length}"]
