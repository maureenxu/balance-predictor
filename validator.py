import base64
import pickle
import pandas as pd
from sklearn.pipeline import Pipeline

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

from src.validate import ModelValidator
from src.configuration import Config

app = FastAPI()


def deserialize_model(serialized_model: str) -> Pipeline:
    return pickle.loads(base64.b64decode(serialized_model.encode('utf-8')))

@app.post("/validate")
async def validate(request: Request, show_plot: bool = False):
    data = await request.json()

    test_data = data['test_data']
    df = pd.DataFrame.from_records(test_data)

    serialized_model = data['model']
    model_pipeline = deserialize_model(serialized_model)

    validator = ModelValidator(Config, df, model_pipeline)
    metrics_dict = validator.get_metrics()

    if show_plot:
        plt = validator.plot_hist_vs_pred()
        print(f"the metrics are: {metrics_dict}")
        plt.show()

    return JSONResponse(content={
        'metrics_dict': metrics_dict,
        'model': serialized_model
    })
