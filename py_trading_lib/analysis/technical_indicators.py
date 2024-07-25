from abc import ABC, abstractmethod

import pandas as pd
import pandas_ta as ta

from py_trading_lib.data_handler.historic_data import KlineChecks


class ITechnicalIndicator(ABC):
    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def calculate(self, klines: pd.DataFrame) -> pd.DataFrame:
        pass

    @abstractmethod
    def get_min_len(self) -> int:
        pass

    def _sanity_checks(self, klines: pd.DataFrame):
        min_len = self.get_min_len()
        KlineChecks().check_columns(klines)
        KlineChecks().check_has_min_len(klines, min_len)


class SMA(ITechnicalIndicator):
    def __init__(self, length: int, offset: int = 0) -> None:
        self.length = length
        self.offset = offset

    def calculate(self, klines: pd.DataFrame) -> pd.DataFrame:
        self._sanity_checks(klines)
        sma = self._try_calculate(klines)
        return sma.to_frame()

    def _try_calculate(self, klines: pd.DataFrame) -> pd.Series:
        try:
            sma = self._calculate_sma(klines)
        except Exception as e:
            raise e

        if not isinstance(sma, pd.Series):
            raise ValueError("Something went wrong during the calculation of the SMA.")

        return sma

    def _calculate_sma(self, klines: pd.DataFrame):
        sma = ta.sma(
            close=klines["CLOSE"],
            length=self.length,
            offset=self.offset,
        )
        return sma

    def get_min_len(self) -> int:
        return self.length


class RSI(ITechnicalIndicator):
    def __init__(
        self, length: int = 14, scalar: float = 100, drift: int = 1, offset: int = 0
    ) -> None:
        self.length = length
        self.scalar = scalar
        self.drift = drift
        self.offset = offset

    def calculate(self, klines: pd.DataFrame) -> pd.DataFrame:
        self._sanity_checks(klines)
        rsi = self._try_calculate(klines)
        return rsi.to_frame()

    def _try_calculate(self, klines: pd.DataFrame) -> pd.Series:
        try:
            rsi = self._calculate_rsi(klines)
        except Exception as e:
            raise e

        if not isinstance(rsi, pd.Series):
            raise ValueError("Something went wrong during the calculation of the RSI.")

        return rsi

    def _calculate_rsi(self, klines: pd.DataFrame):
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
