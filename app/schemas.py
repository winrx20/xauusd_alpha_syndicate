from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class Candle(BaseModel):
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float

class MarketHistory(BaseModel):
    symbol: str
    interval: str
    candles: List[Candle]

class Signal(BaseModel):
    symbol: str
    signal: str
    confidence: float
    score: float
    price: float
    timestamp: datetime
    reasons: List[str]
    risk_level: str

class Trade(BaseModel):
    id: int
    symbol: str
    side: str
    entry_price: float
    size: float
    stop_loss: Optional[float]
    take_profit: Optional[float]
    timestamp: datetime
    closed: bool = False
    exit_price: Optional[float] = None
    pnl: Optional[float] = None

class PaperStatus(BaseModel):
    running: bool
    balance: float
    equity: float
    positions: List[Trade]

