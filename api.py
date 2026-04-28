from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, StrictStr

from sentiment_mini_project import predict_sentiment


app = FastAPI(
    title="Sentiment Analysis Mini API",
    description="Simple NLP sentiment API using TextBlob.",
    version="1.0.0",
)


class PredictRequest(BaseModel):
    text: StrictStr


class BatchPredictRequest(BaseModel):
    texts: list[StrictStr]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(payload: PredictRequest):
    try:
        return predict_sentiment(payload.text)
    except (TypeError, ValueError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/predict/batch")
def predict_batch(payload: BatchPredictRequest):
    if not payload.texts:
        raise HTTPException(status_code=400, detail="Input list cannot be empty.")

    results = []
    errors = []

    for index, text in enumerate(payload.texts):
        try:
            results.append({"index": index, **predict_sentiment(text)})
        except (TypeError, ValueError) as exc:
            errors.append({"index": index, "error": str(exc)})

    return {"results": results, "errors": errors}
