from fastapi import FastAPI
from pydantic import BaseModel, Field
import numpy as np
from sklearn.linear_model import LogisticRegression

app = FastAPI(title="ml-signals")
_model = None

class PredictIn(BaseModel):
    symbol: str = "BTC"
    prices: list[float] = Field(..., min_items=20)

class PredictOut(BaseModel):
    symbol: str
    signal: str
    prob_buy: float
    prob_sell: float

def _features_from_prices(p):
    p = np.asarray(p, dtype=float)
    ret = np.diff(p) / p[:-1]
    sma5 = np.convolve(p, np.ones(5)/5, mode="valid")
    sma10 = np.convolve(p, np.ones(10)/10, mode="valid")
    L = min(len(ret), len(sma5), len(sma10))
    X = np.column_stack([
        ret[-L:],
        sma5[-L:] / p[-L- (len(p)-L):],
        sma10[-L:] / p[-L- (len(p)-L):],
        np.std(ret[-L:]) * np.ones(L),
    ])
    y = np.where((sma5[-L:] > sma10[-L:]) & (ret[-L:] > 0), 2, 1)
    y = np.where((sma5[-L:] < sma10[-L:]) & (ret[-L:] < 0), 0, y)
    return X, y

def _train_synth():
    rng = np.random.default_rng(7)
    Xs, ys = [], []
    for _ in range(20):
        base = 100 + rng.normal(0, 1, 80).cumsum()
        X, y = _features_from_prices(base)
        Xs.append(X); ys.append(y)
    X = np.vstack(Xs); y = np.concatenate(ys)
    clf = LogisticRegression(max_iter=200)
    clf.fit(X, y)
    return clf

@app.on_event("startup")
def _load():
    global _model
    _model = _train_synth()

@app.get("/healthz")
def healthz():
    return {"status": "ok", "service": "ml-signals"}

@app.post("/predict", response_model=PredictOut)
def predict(payload: PredictIn):
    X, _ = _features_from_prices(payload.prices)
    probs = _model.predict_proba(X[-1:])[0]
    idx = int(np.argmax(probs))
    signal = ["sell","hold","buy"][idx]
    return PredictOut(symbol=payload.symbol.upper(), signal=signal, prob_buy=float(probs[2]), prob_sell=float(probs[0]))
