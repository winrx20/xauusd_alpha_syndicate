import pytest
from app.signal import SignalEngine
from app.market import CSVMarketProvider

@pytest.fixture
def hist():
    p = CSVMarketProvider(path="data/xauusd_sample.csv")
    return p.get_history(period=120)

def test_signal_generate(hist):
    se = SignalEngine()
    res = se.generate(hist)
    assert "signal" in res
    assert res["confidence"] >= 0.0 and res["confidence"] <= 1.0
