# Crypto & Stocks Dashboard — 5 Services (Github Qctions)

This repo hosts 6 containerized services you can wire to a Jenkins CI/CD pipeline later.

## Services
- `auth` — demo login / JWT
- `crypto-prices` — mock quotes for BTC/ETH/SOL
- `stocks-prices` — mock quotes for AAPL/MSFT/NVDA
- `portfolio` — in-memory holdings + fake P/L
- `ml-signals` — tiny ML classifier: buy/hold/sell
- `gateway` — NGINX router for unified entry point

## Run locally
```bash
docker compose build --parallel
docker compose up -d
```

Visit:
- Gateway health: http://localhost:8080/healthz
- Auth login: `POST http://localhost:8080/auth/login {"username":"u","password":"p"}`
- Crypto quote: `GET http://localhost:8080/crypto/quote?symbol=BTC`
- Stocks quote: `GET http://localhost:8080/stocks/quote?symbol=AAPL`
- Portfolio P/L: `GET http://localhost:8080/portfolio/pnl?user=alice`
- ML signal: `POST http://localhost:8080/ml/predict` with JSON body:
```json
{ "symbol": "BTC", "prices": [30000,30100,30050,30200,30350,30400,30550,30600,30500,30700,30850,30900,31000,30950,31100,31250,31300,31400,31350,31500] }
```
