from datetime import datetime
from os import listdir
from os.path import isfile, join, dirname, abspath

import socket
import json
import base64
import pickle

from sklearn.pipeline import Pipeline
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import JSONResponse

from src.score import Scorer
from src.configuration import Config

from .utils import pickle_deserialize

app = FastAPI()
active_model = None


def get_latest_model():
    ROOT_DIR = dirname(abspath(__file__))  # This is your Project Root
    MODELS_FOLDER = f"{ROOT_DIR}/../models"
    model_filepaths = [
        f for f in listdir(MODELS_FOLDER) if isfile(join(MODELS_FOLDER, f))
    ]

    if len(model_filepaths) == 0:
        return None

    if len(model_filepaths) == 1:
        with open(
            f"{MODELS_FOLDER}/{model_filepaths[0]}", "r", encoding="utf-8"
        ) as model_file:
            model_pipeline = json.loads(model_file.read())

        return pickle_deserialize(model_pipeline["model_data"]["out"]["model"])

    models = []
    for model_filepath in model_filepaths:
        with open(
            f"{MODELS_FOLDER}/{model_filepath}", "r", encoding="utf-8"
        ) as model_file:
            model_pipeline = json.loads(model_file.read())
            model_pipeline["model_data"]["datetime"] = datetime.strptime(
                model_pipeline["model_data"]["datetime"], "%Y-%m-%dT%H:%M:%S%z"
            )
            models.append(model_pipeline)

    latest_model = sorted(lambda x: x["datetime"], models)[0]
    return pickle_deserialize(latest_model["model_data"]["out"]["model"])


@app.on_event("startup")
async def startup_event():
    global active_model
    active_model = get_latest_model()


@app.post("/score")
async def score(request: Request):
    data = await request.json()

    balance_history = data["balance_history"]
    model_pipeline = None
    if "model" in data:
        serialized_model = data["model"]
        model_pipeline = pickle_deserialize(serialized_model)
    else:
        model_pipeline = active_model

    if model_pipeline is None:
        raise HTTPException(
            status_code=400, detail="Model is not passed, nor is there an active model."
        )

    scorer = Scorer(Config, balance_history, model_pipeline)
    feature_array = scorer.prepare_feature_array()

    score = scorer.get_prediction(feature_array)

    return JSONResponse(status_code=200, content={"scores": score[0]})


@app.post("/submit")
async def submit_model(request: Request):
    """
    Demo purposes only:
    """
    global active_model

    data = await request.json()
    serialized_model = data["model"]
    model_pipeline = pickle_deserialize(serialized_model)

    if not isinstance(model_pipeline, Pipeline):
        return Response(status_code=400)

    active_model = model_pipeline
    return Response(status_code=200)
