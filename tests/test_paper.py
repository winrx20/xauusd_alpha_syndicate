import pytest
from app.paper import PaperTradingEngine

def test_engine_lifecycle():
    e = PaperTradingEngine()
    e.start()
    assert e.running
    e.stop()
    assert not e.running

def test_open_close_trade():
    e = PaperTradingEngine()
    t = e.open_trade("XAUUSD","BUY",1950,1,stop_loss=1940,take_profit=1960)
    assert t["id"] == 1
    closed = e.close_trade(1,1960)
    assert closed is not None
    assert closed["pnl"] is not None
