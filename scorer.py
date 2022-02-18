import json
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler
import os
import pickle
import configparser
from typing import Any, List

from fastapi import FastAPI, Request, Response, BaseModel
from fastapi.response import JSONResponse

from src.score import Scorer
from src.configuration import Config

app = FastAPI()

def load_model(model_params) -> Pipeline:
    model = Config.MODEL.set_params(**Config.PARAMS)
    model_pipeline = Pipeline(
        steps=[("scaler", MinMaxScaler()), ("model", model)]
    )
    model_pipeline.set_params(**model_params)
    return model_pipeline

@app.post("/Score")
async def score(request: Request, balance_history: str, trained_model: BalanceModel):
    from sklearn.preprocessing import MinMaxScaler
    data = json.loads(balance_history)

    scorer = Scorer(Config, data, trained_model)
    feature_array = scorer.prepare_feature_array()
    
    score = scorer.get_prediction(feature_array)
    
    return JSONResponse(status_code=200, data={
        "scores": score
    })
