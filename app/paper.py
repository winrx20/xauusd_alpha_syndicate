import threading
import time
from typing import List, Dict, Any
from .schemas import Trade
from .config import settings
from datetime import datetime

class PaperTradingEngine:
    def __init__(self):
        self.running = False
        self.balance = 10000.0
        self.equity = self.balance
        self.positions: List[Dict[str, Any]] = []
        self.trades: List[Dict[str, Any]] = []
        self.lock = threading.Lock()
        self._worker = None

    def start(self):
        if self.running:
            return
        self.running = True
        self._worker = threading.Thread(target=self._run, daemon=True)
        self._worker.start()

    def stop(self):
        self.running = False
        if self._worker:
            self._worker.join(timeout=2)
            self._worker = None

    def reset(self):
        with self.lock:
            self.balance = 10000.0
            self.equity = self.balance
            self.positions = []
            self.trades = []

    def _run(self):
        while self.running:
            # placeholder for periodic processing
            time.sleep(0.5)

    def status(self):
        return {
            "running": self.running,
            "balance": self.balance,
            "equity": self.equity,
            "open_positions": len(self.positions),
            "closed_trades": len(self.trades),
        }

    def open_trade(self, symbol, side, price, size, stop_loss=None, take_profit=None):
        with self.lock:
            trade = {
                "id": len(self.trades) + 1,
                "symbol": symbol,
                "side": side,
                "entry_price": price,
                "size": size,
                "stop_loss": stop_loss,
                "take_profit": take_profit,
                "timestamp": datetime.utcnow().isoformat(),
                "closed": False,
            }
            self.positions.append(trade)
            self.trades.append(trade)
            return trade

    def close_trade(self, trade_id, exit_price):
        with self.lock:
            for p in self.positions:
                if p["id"] == trade_id and not p.get("closed"):
                    p["closed"] = True
                    p["exit_price"] = exit_price
                    pnl = (exit_price - p["entry_price"]) * p["size"]
                    if p["side"] == "SELL":
                        pnl = -pnl
                    p["pnl"] = pnl
                    self.equity += pnl
                    try:
                        self.positions.remove(p)
                    except ValueError:
                        pass
                    return p
            return None
