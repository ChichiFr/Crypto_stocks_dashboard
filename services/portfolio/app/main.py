from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, List

app = FastAPI(title="portfolio")
# In-memory mock storage for demo
_holdings = {"alice": [{"asset": "BTC", "qty": 0.5}, {"asset": "AAPL", "qty": 3}]}

class Holding(BaseModel):
    asset: str
    qty: float

@app.get("/healthz")
def healthz():
    return {"Status": "ok", "service": "portfolio"}

@app.get("/holdings")
def get_holdings(user: str = "alice") -> Dict[str, List[Holding]]:
    return {"user": user, "holdings": _holdings.get(user, [])}

@app.post("/holdings")
def add_holding(user: str, item: Holding):
    _holdings.setdefault(user, []).append(item.model_dump())
    return {"ok": True, "count": len(_holdings[user])}

@app.get("/pnl")
def pnl(user: str = "alice"):
    # Fake P/L just for demo
    return {"user": user, "pnlUsd": 123.45}
