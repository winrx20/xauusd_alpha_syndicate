from .config import settings

class RiskEngine:
    def __init__(self):
        self.risk_per_trade = settings.RISK_PER_TRADE
        self.max_daily_loss = settings.MAX_DAILY_LOSS
        self.max_drawdown = settings.MAX_DRAWDOWN
        self.default_rr = settings.DEFAULT_RISK_REWARD

    def position_size(self, balance: float, entry_price: float, stop_loss: float):
        # Simple USD risk sizing: risk_per_trade% of balance
        if stop_loss is None or stop_loss <= 0 or entry_price <= 0:
            return 0.0
        risk_amount = balance * self.risk_per_trade
        # size in units (not contracts): risk_amount / (abs(entry - stop) )
        stop_distance = abs(entry_price - stop_loss)
        if stop_distance == 0:
            return 0.0
        size = risk_amount / stop_distance
        return size

    def validate_trade(self, balance: float, entry_price: float, stop_loss: float):
        size = self.position_size(balance, entry_price, stop_loss)
        if size <= 0:
            return False, "Invalid position size"
        # other checks can be added
        return True, None
