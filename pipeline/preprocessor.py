from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse

from src import preprocess
from src.configuration import Config

from .utils import add_metadata

app = FastAPI()


@app.post("/preprocess")
async def preprocesser(request: Request):
    data = await request.json()
    preprocessor = preprocess.DataPreprocessor(Config, data)
    df_output = preprocessor.preprocess()
    return JSONResponse(content=add_metadata(df_output.to_dict(orient="records")))
