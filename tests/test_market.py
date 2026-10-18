import pytest
from app.market import CSVMarketProvider

@pytest.fixture
def provider():
    return CSVMarketProvider(path="data/xauusd_sample.csv")

def test_get_latest(provider):
    latest = provider.get_latest()
    assert latest is not None
    assert "close" in latest

def test_get_history(provider):
    h = provider.get_history(period=10)
    assert len(h) == 10

def test_empty_provider(tmp_path):
    p = CSVMarketProvider(path=str(tmp_path / "nofile.csv"))
    assert p.get_latest() is None
    assert p.get_history() == []
