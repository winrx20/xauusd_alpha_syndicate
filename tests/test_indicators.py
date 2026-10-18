import pytest
from app.indicators import sma, ema, rsi, macd, atr, bollinger_bands

def test_sma():
    s = [1,2,3,4,5]
    assert sma(s, 3) == pytest.approx(4.0)

def test_ema():
    s = [1,2,3,4,5,6,7,8]
    assert ema(s, 3) is not None

def test_rsi_insufficient():
    s = [1,2,3]
    assert rsi(s, 14) is None

def test_macd():
    s = list(range(1,60))
    assert macd(s) is not None

def test_atr_insufficient():
    highs=[1,2,3]
    lows=[0.5,1.5,2.5]
    closes=[0.9,1.8,2.7]
    assert atr(highs,lows,closes,14) is None

