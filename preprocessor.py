import json
import configparser

from fastapi import FastAPI, Request, Response

from src.preprocess import DataPreprocessor
from src.utils import *
from src.configuration import Config

app = FastAPI()

config = configparser.ConfigParser()
config.read_file("pipeline.config")


@app.get("/start_preprocessing")
async def preprocess(request: Request):
    config = request.app.state.config

    input_path = os.path.join(
        config["DEFAULT"]["base_path"], config["PREPROCESSING"]["input_path"]
    )
    with open(input_path) as input_file:
        data = json.load(input_file)

    preprocessor = DataPreprocessor(config=Config, data=data)
    df_output = preprocessor.preprocess()

    pickle_dump_output(
        config["DEFAULT"]["base_path"],
        config["PREPROCESSING"]["output_path"],
        df_output,
    )

    return Response(status_code=200)
