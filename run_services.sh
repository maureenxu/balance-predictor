#!/bin/bash

. .venv/bin/activate
uvicorn preprocessor:app --reload &
uvicorn splitter:app --reload --port 8001 &
uvicorn trainer:app --reload --port 8002 &
uvicorn validator:app --reload --port 8003
deactivate