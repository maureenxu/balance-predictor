import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler

import sklearn_json as skljson

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

from src.validate import ModelValidator
from src.configuration import Config

app = FastAPI()


def load_model(model_params) -> Pipeline:
    model = Config.MODEL.set_params(**Config.PARAMS)
    model_pipeline = Pipeline(
        steps=[("scaler", MinMaxScaler()), ("model", model)]
    )
    model_pipeline.set_params(**model_params)
    return model_pipeline

@app.post("/validate")
async def validate(request: Request):
    data = await request.json()

    test_data = data['test_data']
    df = pd.DataFrame.from_records(test_data)

    model_params = data['model']
    print(load_model(model_params))

    return Response(200)
    # model_pipeline = model_params_loader(model_params)

    # validator = ModelValidator(Config, df, model_pipeline)
    # metrics_dict = validator.get_metrics()

    # # plt = validator.plot_hist_vs_pred()
    # # print(f"the metrics are: {metrics_dict}")
    # # plt.savefig(fname=some_output_path)

    # return JSONResponse(content={
    #     'metrics_dict': metrics_dict
    # })
