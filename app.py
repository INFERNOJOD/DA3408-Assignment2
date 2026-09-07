from fastapi import FastAPI
from pydantic import BaseModel
import joblib

app = FastAPI()

model = joblib.load("model.joblib")


class PredictionRequest(BaseModel):
    text: str


@app.post("/predict")
def predict(request: PredictionRequest):
    label = model.predict([request.text])[0]
    return {"label": label}


@app.get("/healthz")
def healthz():
    return {"status": "ok"}
