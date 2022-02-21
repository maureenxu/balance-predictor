from datetime import datetime
import importlib.metadata

import base64
import pickle
import pandas as pd
from sklearn.pipeline import Pipeline

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.validate import ModelValidator
from src.configuration import Config

app = FastAPI()
__version__ = importlib.metadata.version("MLOps-BalancePredictor-demo")


def add_metadata(content: dict):
    return {
        "out": content,
        "datetime": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S%z"),
        "version": __version__,
    }


def pickle_deserialize(serialized_obj: str) -> Pipeline:
    return pickle.loads(base64.b64decode(serialized_obj.encode("utf-8")))


def pickle_serialize(obj: object):
    return base64.b64encode(pickle.dumps(obj)).decode("utf-8")


@app.post("/validate")
async def validate(request: Request):
    data = await request.json()

    test_data = data["test_data"]
    df = pd.DataFrame.from_records(test_data)

    serialized_model = data["model"]
    model_pipeline = pickle_deserialize(serialized_model)

    validator = ModelValidator(Config, df, model_pipeline)
    metrics_dict = validator.get_metrics()

    plt = validator.plot_hist_vs_pred()
    serialized_plt = pickle_serialize(plt.gcf())

    return JSONResponse(
        content=add_metadata(
            {
                "metrics_dict": metrics_dict,
                "model": serialized_model,
                "validate_plot": serialized_plt,
            }
        )
    )
