from fastapi import FastAPI
from typing import Dict

app = FastAPI(title="crypto-prices")

@app.get("/healthz")
def healthz():
    return {"status": "ok", "service": "crypto-prices"}

# Mock endpoint; replace with real exchange API later
@app.get("/quote")
def quote(symbol: str = "BTC") -> Dict[str, float]:
    fake = {"BTC": 68000.0, "ETH": 3500.0, "SOL": 180.0}
    return {"symbol": symbol.upper(), "usd": fake.get(symbol.upper(), 100.0)}

