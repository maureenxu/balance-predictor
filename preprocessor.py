from enum import Enum

import configparser
from typing import List

from pydantic import BaseModel
from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse

from src import preprocess
from src.configuration import Config

app = FastAPI()


@app.post("/preprocess")
async def preprocesser(request: Request):
    data = await request.json()
    preprocessor = preprocess.DataPreprocessor(Config, data)
    df_output = preprocessor.preprocess()
    return JSONResponse(content=df_output.to_dict(orient="records"))
