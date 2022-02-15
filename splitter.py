import pandas as pd
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.split import DataSpliter
from src.configuration import Config

app = FastAPI()

@app.post("/split")
async def split(request: Request):
    data = await request.json()
    df = pd.DataFrame.from_records(data)

    splitter = DataSpliter(Config, df)
    df_train, df_test = splitter.split(split_ratio=0.8)

    return JSONResponse(content={
        'train': df_train.to_dict(orient='records'),
        'test': df_test.to_dict(orient='records')
    })
