import os
import pickle
import configparser

from fastapi import FastAPI, Request, Response

from src import train, utils

app = FastAPI()

config = configparser.ConfigParser()
config.read_file("pipeline.config")


@app.get("/start_training")
async def train(request: Request):
    config = request.app.state.config

    input_path = os.path.join(
        config["DEFAULT"]["base_path"], config["TRAINER"]["input_path"]
    )
    with open(input_path, "rb") as input_file:
        df = pickle.load(input_file)

    trainer = train.ModelTrainer(df, config.PARAMS)
    cv_results = trainer.cross_validate()
    model_pipeline = trainer.train_model()

    print(f"the cross validation results are: {cv_results}")

    utils.pickle_dump_output(
        config["DEFAULT"]["base_path"], config["TRAINER"]["output_path"], model_pipeline
    )

    return Response(status_code=200)
