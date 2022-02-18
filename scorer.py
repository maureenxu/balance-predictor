import base64
import json
from sklearn.pipeline import Pipeline
import pickle

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.score import Scorer
from src.configuration import Config

app = FastAPI()

def deserialize_model(serialized_model: str) -> Pipeline:
    return pickle.loads(base64.b64decode(serialized_model.encode('utf-8')))


@app.post("/score")
async def score(request: Request):
    data = await request.json()

    balance_history = data['balance_history']
    input_data = json.loads(balance_history)

    serialized_model = data['model']
    model_pipeline = deserialize_model(serialized_model)

    scorer = Scorer(Config, input_data, model_pipeline)
    feature_array = scorer.prepare_feature_array()
    
    score = scorer.get_prediction(feature_array)
    
    return JSONResponse(status_code=200, data={
        "scores": score
    })
