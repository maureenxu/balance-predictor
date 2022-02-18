import json
import base64
import pickle
import typing

import numpy
import pandas as pd

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sklearn.pipeline import Pipeline

from src.train import ModelTrainer
from src.configuration import Config

app = FastAPI()

class JSONModelResponse(JSONResponse):
    media_type = "application/json"

    def _default_dumps(self, val):
        if isinstance(val, numpy.ndarray):
            return list(val)

    def render(self, content: typing.Any) -> bytes:
        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(",", ":"),
            default=self._default_dumps
        ).encode("utf-8")


def serialize_model(model_pipeline: Pipeline) -> str:
    return base64.b64encode(pickle.dumps(model_pipeline)).decode('utf-8')


@app.post("/train")
async def train(request: Request):
    data = await request.json()
    df = pd.DataFrame.from_records(data)
    
    trainer = ModelTrainer(Config, df)
    cv_results = trainer.cross_validate()
    model_pipeline = trainer.train_model()

    return JSONModelResponse(
        content={
        "cv_result": cv_results,
        "model": serialize_model(model_pipeline)
    })
