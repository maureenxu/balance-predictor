import json
import os
import pickle
import configparser
from typing import Any, List

from fastapi import FastAPI, Request, Response, BaseModel
from fastapi.response import JSONResponse
from sklearn.ensemble import RandomForestRegressor

from src.score import Scorer
from src.configuration import Config

app = FastAPI()

# TODO: Define BalanceModel type
BalanceModel = RandomForestRegressor


@app.post("/start_scoring")
async def score(request: Request, balance_history: str, trained_model: BalanceModel):
    data = json.loads(balance_history)

    scorer = Scorer(Config, data, trained_model)
    feature_array = scorer.prepare_feature_array()
    
    score = scorer.get_prediction(feature_array)
    
    return JSONResponse(status_code=200, data={
        "scores": score
    })
