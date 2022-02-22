uvicorn pipeline.preprocessor:app --host 0.0.0.0 --port 8000 &
    uvicorn pipeline.splitter:app --host 0.0.0.0 --port 8001 &
    uvicorn pipeline.trainer:app --host 0.0.0.0 --port 8002 &
    uvicorn pipeline.validator:app --host 0.0.0.0 --port 8003 &
    uvicorn pipeline.scorer:app --host 0.0.0.0 --port 8004
