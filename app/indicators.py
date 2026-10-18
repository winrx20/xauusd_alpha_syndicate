import numpy as np
import pandas as pd

def sma(series, period):
    s = pd.Series(series).astype(float)
    if len(s) < period:
        return None
    return s.rolling(window=period).mean().iloc[-1]

def ema(series, period):
    s = pd.Series(series).astype(float)
    if len(s) < period:
        return None
    return s.ewm(span=period, adjust=False).mean().iloc[-1]

def rsi(series, period=14):
    s = pd.Series(series).astype(float)
    if len(s) < period + 1:
        return None
    delta = s.diff().dropna()
    up = delta.clip(lower=0).rolling(window=period).mean()
    down = -1 * delta.clip(upper=0).rolling(window=period).mean()
    rs = up / down
    rsi = 100 - (100 / (1 + rs))
    return float(rsi.iloc[-1]) if not np.isnan(rsi.iloc[-1]) else None

def macd(series, fast=12, slow=26, signal=9):
    s = pd.Series(series).astype(float)
    if len(s) < slow + signal:
        return None
    ema_fast = s.ewm(span=fast, adjust=False).mean()
    ema_slow = s.ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    hist = macd_line - signal_line
    return {"macd": float(macd_line.iloc[-1]), "signal": float(signal_line.iloc[-1]), "hist": float(hist.iloc[-1])}

def atr(highs, lows, closes, period=14):
    h = pd.Series(highs).astype(float)
    l = pd.Series(lows).astype(float)
    c = pd.Series(closes).astype(float)
    if len(c) < period + 1:
        return None
    tr1 = h - l
    tr2 = (h - c.shift()).abs()
    tr3 = (l - c.shift()).abs()
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr_val = tr.rolling(window=period).mean().iloc[-1]
    return float(atr_val)

def bollinger_bands(series, period=20, stds=2):
    s = pd.Series(series).astype(float)
    if len(s) < period:
        return None
    ma = s.rolling(window=period).mean()
    sd = s.rolling(window=period).std()
    last = len(s) - 1
    return {"middle": float(ma.iloc[-1]), "upper": float(ma.iloc[-1] + stds * sd.iloc[-1]), "lower": float(ma.iloc[-1] - stds * sd.iloc[-1])}

