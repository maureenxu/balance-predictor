import os
import pickle
import configparser
from typing import Any, List

from fastapi import FastAPI, Request, Response, BaseModel
from fastapi.response import JSONResponse

from src import train, utils

app = FastAPI()

BalanceHistory = List[int]

# TODO: Define BalanceModel type
BalanceModel = Any


@app.post("/start_scoring")
async def score(request: Request, balance_history: BalanceHistory, trained_model: BalanceModel):
    scores = trained_model.predict(balance_history)

    return JSONResponse(status_code=200, data= {
        "scores": scores
    })
