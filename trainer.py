import json
import typing

import numpy
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import sklearn_json as skljson

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.train import ModelTrainer
from src.configuration import Config

app = FastAPI()

class JSONModelResponse(JSONResponse):
    media_type = "application/json"

    def _default_dumps(self, val):
        if isinstance(val, numpy.ndarray):
            return list(val)

        if isinstance(val, RandomForestRegressor):
            return skljson.to_dict(val)
        
        return val.__dict__

    def render(self, content: typing.Any) -> bytes:
        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(",", ":"),
            default=self._default_dumps
        ).encode("utf-8")


@app.post("/train")
async def train(request: Request):
    data = await request.json()
    df = pd.DataFrame.from_records(data)
    
    trainer = ModelTrainer(Config, df)
    cv_results = trainer.cross_validate()
    model_pipeline = trainer.train_model()

    print(f"the cross validation results are: {cv_results}")

    ## TODO: 1) pickle + base64 (or parameters)
    return JSONModelResponse(
        content={
        "cv_result": cv_results,
        "model": dict(model_pipeline.get_params())
    })
