# A script we use during development, as it is faster than docker image building. 
uvicorn pipeline.preprocessor:app --host 0.0.0.0 --port 8000 --reload &
    uvicorn pipeline.splitter:app --host 0.0.0.0 --port 8001 --reload  &
    uvicorn pipeline.trainer:app --host 0.0.0.0 --port 8002 --reload  &
    uvicorn pipeline.validator:app --host 0.0.0.0 --port 8003 --reload  &
    uvicorn pipeline.scorer:app --host 0.0.0.0 --port 8004 --reload 
