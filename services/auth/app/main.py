from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from jose import jwt
from datetime import datetime, timedelta
import os

SECRET = os.getenv("JWT_SECRET", "dev-secret")
ALGO = "HS256"

app = FastAPI(title="auth")

class LoginIn(BaseModel):
    username: str
    password: str

@app.get("/healthz")
def healthz():
    return {"status": "ok", "service": "luth"}

@app.post("/login")
def login(payload: LoginIn):
    if not payload.username or not payload.password:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = jwt.encode({"sub": payload.username, "exp": datetime.utcnow() + timedelta(hours=1)}, SECRET, algorithm=ALGO)
    return {"access": token}
