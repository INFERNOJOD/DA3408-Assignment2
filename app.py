from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import redis

app = FastAPI()

model = joblib.load("model.joblib")

cache = redis.Redis(host="cache", port=6379, decode_responses=True)

class PredictionRequest(BaseModel):
    text: str

@app.post("/predict")
def predict(request: PredictionRequest):
    cached_label = cache.get(request.text)

    if cached_label is not None:
        return {"label": cached_label}

    label = model.predict([request.text])[0]

    cache.set(request.text, label, ex=300)

    return {"label": label}

@app.get("/healthz")
def healthz():
    return {"status": "ok"}
