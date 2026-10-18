import pandas as pd
from abc import ABC, abstractmethod
from typing import List
from .config import settings
from datetime import datetime

class MarketDataProvider(ABC):
    @abstractmethod
    def get_latest(self, symbol: str):
        pass

    @abstractmethod
    def get_history(self, symbol: str, interval: str, period: int = 100):
        pass

class CSVMarketProvider(MarketDataProvider):
    def __init__(self, path: str = None):
        self.path = path or settings.MARKET_CSV_PATH
        self._df = None
        self._load()

    def _load(self):
        try:
            self._df = pd.read_csv(self.path, parse_dates=["timestamp"])
            # ensure sorted
            self._df = self._df.sort_values("timestamp").reset_index(drop=True)
        except Exception:
            self._df = pd.DataFrame(columns=["timestamp","open","high","low","close","volume"])

    def get_latest(self, symbol: str = None):
        if self._df is None or self._df.empty:
            return None
        row = self._df.iloc[-1]
        return row.to_dict()

    def get_history(self, symbol: str = None, interval: str = None, period: int = 100):
        # ignore interval for CSV provider; return last `period` candles
        if self._df is None or self._df.empty:
            return []
        df = self._df.tail(period).copy()
        # validate
        df = df.dropna()
        out = df.to_dict(orient="records")
        return out

# Factory

def get_default_provider():
    if settings.MARKET_PROVIDER == "csv":
        return CSVMarketProvider()
    # placeholder for future providers
    return CSVMarketProvider()
