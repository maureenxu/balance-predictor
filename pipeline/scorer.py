import base64
import importlib.metadata
from datetime import datetime
import json
import pickle

from sklearn.pipeline import Pipeline
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.score import Scorer
from src.configuration import Config

app = FastAPI()
__version__ = importlib.metadata.version("MLOps-BalancePredictor-demo")

def add_metadata(content: dict):
    return {
        "out": content,
        "datetime": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S%z"),
        "version": __version__,
    }

def pickle_deserialize(serialized_obj: str) -> Pipeline:
    return pickle.loads(base64.b64decode(serialized_obj.encode("utf-8")))


@app.post("/score")
async def score(request: Request):
    data = await request.json()

    balance_history = data['balance_history']

    serialized_model = data['model']
    model_pipeline = pickle_deserialize(serialized_model)

    scorer = Scorer(Config, balance_history, model_pipeline)
    feature_array = scorer.prepare_feature_array()
    
    score = scorer.get_prediction(feature_array)
    
    return JSONResponse(status_code=200, content={
        "scores": score,
        "model": serialized_model
    })
