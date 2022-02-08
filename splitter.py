import os
import pickle
import configparser

from fastapi import FastAPI, Request, Response

from src import split, utils

app = FastAPI()

config = configparser.ConfigParser()
config.read_file("pipeline.config")


@app.get("/start_splitting")
async def split(request: Request):
    config = request.app.state.config

    input_path = os.path.join(
        config["DEFAULT"]["base_path"], config["SPLITTER"]["input_path"]
    )

    with open(input_path, "rb") as input_file:
        df = pickle.load(input_file)

    spliter = split.DataSpliter(df, config["SPLITTER"]["split_ratio"])
    df_train, df_test = spliter.split()

    utils.pickle_dump_output(
        config["DEFAULT"]["base_path"],
        config["SPLITTER"]["output_train_path"],
        df_train,
    )

    utils.pickle_dump_output(
        config["DEFAULT"]["base_path"],
        config["SPLITTER"]["output_test_path"],
        df_test,
    )

    request.get("trainer.localhost:8010/start_training")
    return Response(200)
