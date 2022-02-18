from datetime import datetime
import importlib.metadata

from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse

from src import preprocess
from src.configuration import Config


app = FastAPI()
__version__ = importlib.metadata.version("MLOps-BalancePredictor-demo")


def add_metadata(content: dict):
    return {
        "out": content,
        "datetime": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S%z"),
        "version": __version__,
    }


@app.post("/preprocess")
async def preprocesser(request: Request):
    data = await request.json()
    preprocessor = preprocess.DataPreprocessor(Config, data)
    df_output = preprocessor.preprocess()
    return JSONResponse(content=add_metadata(df_output.to_dict(orient="records")))
