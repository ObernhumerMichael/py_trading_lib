from abc import ABC, abstractmethod
from typing import List

import pandas as pd
import pandas_ta as ta

import py_trading_lib.utils.sanity_checks as sanity
import py_trading_lib.utils.utils as utils


__all__ = ["TechnicalIndicator", "SMA", "RSI"]


class TechnicalIndicator(ABC):
    def calculate(self, tohlcv: pd.DataFrame) -> pd.DataFrame:
        self._perfrom_sanity_checks(tohlcv)
        indicator = self._try_calculate(tohlcv)
        return indicator

    def _perfrom_sanity_checks(self, tohlcv: pd.DataFrame):
        sanity.check_tohlcv(tohlcv)
        min_len = self.get_min_len()
        sanity.check_has_min_len(tohlcv, min_len)

    def _try_calculate(self, klines: pd.DataFrame) -> pd.DataFrame:
        try:
            indicator = self._calculate_indicator(klines)
        except Exception as e:
            raise RuntimeError(
                f"Something went wrong during the calculation of the indicator: {self.get_names()}. {e}"
            )

        return indicator

    @abstractmethod
    def _calculate_indicator(self, klines: pd.DataFrame) -> pd.DataFrame:
        pass

    @abstractmethod
    def get_names(self) -> List[str]:
        pass

    @abstractmethod
    def get_min_len(self) -> int:
        pass


class SMA(TechnicalIndicator):
    def __init__(self, length: int, offset: int = 0) -> None:
        self._length = length
        self._offset = offset

    def _calculate_indicator(self, klines: pd.DataFrame) -> pd.DataFrame:
        sma = ta.sma(
            close=klines["CLOSE"],
            length=self._length,
            offset=self._offset,
        )
        sma = utils.convert_to_df_from_sr_or_df(sma)
        return sma

    def get_min_len(self) -> int:
        return self._length

    def get_names(self) -> List[str]:
        """
        Example return: ["SMA_5"]
        """
        return [f"SMA_{self._length}"]


class RSI(TechnicalIndicator):
    def __init__(
        self, length: int = 14, scalar: float = 100, drift: int = 1, offset: int = 0
    ) -> None:
        self._length = length
        self._scalar = scalar
        self._drift = drift
        self._offset = offset

    def _calculate_indicator(self, klines: pd.DataFrame) -> pd.DataFrame:
        rsi = ta.rsi(
            close=klines["CLOSE"],
            length=self._length,
            scalar=self._scalar,
            drift=self._drift,
            offset=self._offset,
        )
        rsi = utils.convert_to_df_from_sr_or_df(rsi)
        return rsi

    def get_min_len(self) -> int:
        return self._length

    def get_names(self) -> List[str]:
        """
        Example return: ["RSI_5"]
        """
        return [f"RSI_{self._length}"]
