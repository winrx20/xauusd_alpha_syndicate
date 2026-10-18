from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse
from .config import settings
from .market import get_default_provider
from .signal import SignalEngine
from .paper import PaperTradingEngine
from .schemas import MarketHistory, Signal
from typing import Any
import uvicorn

app = FastAPI(title="XAUUSD Alpha Syndicate API")

provider = get_default_provider()
signal_engine = SignalEngine()
paper_engine = PaperTradingEngine()

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/api/market")
async def api_market():
    hist = provider.get_history(settings.MARKET_SYMBOL, settings.MARKET_INTERVAL, period=200)
    return {"symbol": settings.MARKET_SYMBOL, "candles": hist[-100:]}

@app.get("/api/signal")
async def api_signal():
    hist = provider.get_history(settings.MARKET_SYMBOL, settings.MARKET_INTERVAL, period=300)
    if not hist or len(hist) < 30:
        raise HTTPException(status_code=400, detail="insufficient data for signal")
    sig = signal_engine.generate(hist)
    return sig

@app.get("/api/paper/status")
async def api_paper_status():
    return paper_engine.status()

@app.get("/api/paper/trades")
async def api_paper_trades():
    return {"trades": paper_engine.trades}

@app.get("/api/paper/positions")
async def api_paper_positions():
    return {"positions": paper_engine.positions}

@app.post("/api/paper/start")
async def api_paper_start():
    paper_engine.start()
    return {"started": True}

@app.post("/api/paper/stop")
async def api_paper_stop():
    paper_engine.stop()
    return {"stopped": True}

@app.post("/api/paper/reset")
async def api_paper_reset():
    paper_engine.reset()
    return {"reset": True}

@app.get("/")
async def root():
    return FileResponse("static/index.html")

if __name__ == "__main__":
    uvicorn.run("app.main:app", host=settings.APP_HOST, port=settings.APP_PORT)
