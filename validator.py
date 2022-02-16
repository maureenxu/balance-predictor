import os
import pickle
import configparser

from fastapi import FastAPI, Request, Response

from.src.configuration import Config
from src.validate import ModelValidator
from src.utils import *

app = FastAPI()

config = configparser.ConfigParser()
config.read_file("pipeline.config")


@app.get("/start_validating")
async def validate(request: Request):
    config = request.app.state.config

    input_test_path = os.path.join(
        config["DEFAULT"]["base_path"], config["VALIDATOR"]["data_path"]
    )
    input_model_path = os.path.join(
        config["DEFAULT"]["base_path"], config["VALIDATOR"]["model_path"]
    )

    with open(input_test_path, "rb") as input_file:
        df = pickle.load(input_file)

    with open(input_model_path, "rb") as input_file:
        model_pipeline = pickle.load(input_file)

    validator = ModelValidator(Config, df, model_pipeline)
    metrics_dict = validator.get_metrics()
    plt = validator.plot_hist_vs_pred()

    print(f"the metrics are: {metrics_dict}")

    pickle_dump_output(
        config["DEFAULT"]["base_path"],
        config["VALIDATOR"]["output_metrics"],
        metrics_dict,
    )

    output_plot_path = os.path.join(
        config["DEFAULT"]["base_path"], config["VALIDATOR"]["output_plot"]
    )
    plt.savefig(fname=output_plot_path)

    return Response(status_code=200)
