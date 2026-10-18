from .indicators import sma, ema, rsi, macd, atr, bollinger_bands
from datetime import datetime
from .config import settings
from typing import Dict, Any

class SignalEngine:
    def __init__(self, weights: Dict[str, float] = None):
        # default weights
        default = {
            "technical_trend": 0.30,
            "momentum": 0.15,
            "volatility": 0.10,
            "news": 0.25,
            "macro": 0.10,
            "regime": 0.10,
        }
        self.weights = weights or default

    def generate(self, history):
        # history: list of candles dicts with close/high/low
        closes = [c["close"] for c in history]
        highs = [c["high"] for c in history]
        lows = [c["low"] for c in history]
        latest = history[-1]
        reasons = []
        score = 0.0

        # trend: EMA(50) vs EMA(200)
        trend_score = 0.0
        e50 = ema(closes, 50)
        e200 = ema(closes, 200)
        if e50 and e200:
            if e50 > e200:
                trend_score = 1.0
                reasons.append("EMA50 > EMA200")
            else:
                trend_score = -1.0
                reasons.append("EMA50 < EMA200")
        # momentum: MACD hist
        momentum_score = 0.0
        mac = macd(closes)
        if mac:
            if mac["hist"] > 0:
                momentum_score = 1.0
                reasons.append("MACD histogram > 0")
            else:
                momentum_score = -1.0
                reasons.append("MACD histogram < 0")
        # volatility: ATR
        vol_score = 0.0
        a = atr(highs, lows, closes)
        if a:
            vol_score = 0.0 # neutral for now

        # combine
        score = (
            self.weights["technical_trend"] * ((trend_score + 1)/2) +
            self.weights["momentum"] * ((momentum_score + 1)/2)
        )
        # normalize to 0-100
        final_score = score * 100
        signal = "HOLD"
        confidence = 0.0
        if final_score > 55:
            signal = "BUY"
            confidence = min(1.0, final_score / 100)
        elif final_score < 45:
            signal = "SELL"
            confidence = min(1.0, (100 - final_score) / 100)
        else:
            signal = "HOLD"
            confidence = 0.5

        return {
            "symbol": settings.MARKET_SYMBOL,
            "signal": signal,
            "confidence": confidence,
            "score": final_score,
            "price": latest["close"],
            "timestamp": datetime.utcnow().isoformat(),
            "reasons": reasons,
            "risk_level": "MEDIUM",
        }
