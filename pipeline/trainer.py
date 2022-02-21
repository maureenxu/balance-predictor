from datetime import datetime
import json
import base64
import importlib.metadata

import pickle
import typing

import numpy
import pandas as pd

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.train import ModelTrainer
from src.configuration import Config

from .utils import add_metadata, pickle_serialize

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
            default=self._default_dumps,
        ).encode("utf-8")


@app.post("/train")
async def train(request: Request):
    data = await request.json()
    df = pd.DataFrame.from_records(data)

    trainer = ModelTrainer(Config, df)
    cv_results = trainer.cross_validate()
    model_pipeline = trainer.train_model()

    return JSONModelResponse(
        content=add_metadata(
            {"cv_result": cv_results, "model": pickle_serialize(model_pipeline)}
        )
    )
