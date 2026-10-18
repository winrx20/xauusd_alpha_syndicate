from pydantic import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    APP_ENV: str = "development"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    PUBLIC_ACCESS: bool = False
    APP_USERNAME: Optional[str] = None
    APP_PASSWORD: Optional[str] = None

    MARKET_SYMBOL: str = "XAUUSD"
    MARKET_PROVIDER: str = "csv"
    MARKET_CSV_PATH: str = "data/xauusd_sample.csv"
    MARKET_INTERVAL: str = "15m"

    PAPER_TRADING: bool = True
    AUTO_ORDER: bool = False

    RISK_PER_TRADE: float = 0.01
    MAX_DAILY_LOSS: float = 0.03
    MAX_DRAWDOWN: float = 0.15
    DEFAULT_RISK_REWARD: float = 2.0

    DB_PATH: str = "data/db.sqlite3"

    class Config:
        env_file = ".env"

settings = Settings()
