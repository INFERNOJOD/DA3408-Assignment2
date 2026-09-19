from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import os
import redis

app = FastAPI()

model = joblib.load("model.joblib")

cache = redis.Redis(
    host=os.getenv("REDIS_HOST", "cache"),
    port=6379,
    decode_responses=True,
    socket_connect_timeout=1
)

class PredictionRequest(BaseModel):
    text: str

@app.post("/predict")
def predict(request: PredictionRequest):
    try:
        cached_label = cache.get(request.text)
        if cached_label is not None:
            return {"label": cached_label}
    except redis.RedisError:
        pass

    label = str(model.predict([request.text])[0])

    try:
        cache.set(request.text, label, ex=300)
    except redis.RedisError:
        pass

    return {"label": label}

@app.get("/healthz")
def healthz():
    return {"status": "ok"}
