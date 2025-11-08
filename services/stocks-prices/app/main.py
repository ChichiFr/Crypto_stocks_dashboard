from fastapi import FastAPI
from typing import Dict

app = FastAPI(title="stocks-prices")

@app.get("/healthz")
def healthz():
    return {"status": "ok", "service": "stocks-prices"}

@app.get("/quote")
def quote(symbol: str = "AAPL") -> Dict[str, float]:
    fake = {"AAPL": 195.0, "MSFT": 430.0, "NVDA": 1200.0}
    return {"symbol": symbol.upper(), "usd": fake.get(symbol.upper(), 100.0)}


