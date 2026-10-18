import pytest
from app.risk import RiskEngine

def test_position_size_invalid():
    r = RiskEngine()
    size = r.position_size(10000, 0, 0)
    assert size == 0.0

def test_validate_trade():
    r = RiskEngine()
    ok, msg = r.validate_trade(10000, 1950, 1900)
    assert ok
