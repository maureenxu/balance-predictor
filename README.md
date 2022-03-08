# balance-predictor
This is a project for demonstrating MLOps, openning up the black box to showcase how in theory it could work. But this is NOT a production-ready project for performing MLOps. It will use a simple balance predictor as an example.

The pipeline for building the predictor is shown in Figure 1. There is a [source code script](./src) for every step, written in Python classes.
There are [tests](./tests) written to ensure every function performs as expected.
Then each module is wrapped to a [service](./pipeline) with an individual endpoint using FastApi.
The orchestration of these services is done in bash scripts.
In addition, Docker is also used for containerising the whole pipeline

![Machine learning pipeline](./images/ml_pipeline.png)
_Figure 1. Machine learning pipeline for building a balance predictor._

# Setting up the project

If for some reason you are not able to run the `make venv` command, please make sure you have performed something similiar to the following steps:

```bash
pip install cython # Expected to be installed by some of our dependencies, but not implicitly installed.
pip install -e . # Editable, local install of the current code base
pip install -r requirements.txt
pip install -r requirements-dev.txt
```
# Running the services using Docker
First, please make sure that you have installed `docker` + `docker-compose`. 

You can run the services you should startup the docker containers. You can do so by running `docker-compose up`. This will start fetching the required docker images, and run the services. 

# Running the pipeline
To run the pipeline/orchestrator we have created 3 utility scripts: `run_pipeline.sh`, `run_pipeline_local.sh`, `run_pipeline_remote.sh`. Where `run_pipeline.sh` contains all orchestrator logic, and the other two are shortcut scripts to tell the `run_pipeline.sh` which server to talk to. We recommend to only use the local version as this code is not a production ready code-base, and is merely build to decompose what MLOps may look like.

To run the pipeline, use `./run_pipeline_local.sh` (make sure the script's got execution rights). If you also want to save the model that has been created by the service use the `-s` option.

Requirement:
1) There is data available: data/train_input.json

# Scoring for a prediction
Use `run_scorer.sh` for scoring a predictions. 
It uses two arguments: 
1) input data (i.e. a new transaction history) 
2) model (optional) If null, the script will pick up the activate one for scoring.

If no model is passed, there must be an active model running in the scorer service. Otherwise, an 400 error is returned.

Read the section below on how to activate a model in the scorer service.

# Submitting a model to the scorer
To submit a model to the scorer you can use the `run_submit_model.sh` script. This scripts requires the modelname, and will search for the model in the current location: `models/{modelname}.json`.

# External Dependencies
The scipy library requires some external packages to be installed. We use the one below for our environments. 
```bash
# OpenSUSE
zypper addrepo https://download.opensuse.org/repositories/science/openSUSE_Tumbleweed/science.repo
zypper install lapack gcc-fortran gcc-c++ 
```

If you miss any libraries for you operating system, feel free to add them to the above list.

# Secrets folder
To prevent arbitrary code to be runnable, we have added symmetric encryption to the serialization of the data. This means that the a key should be generated. We require a libsodium key to be generated, in the `secrets/secret.key`. To generate such a key, we have included a simple tool script. Runnable using `python -m tools.generate_key secrets/secret.key`.

Two requirements:
1) You have the correct packages installed (or are in this projects virtual environment)
2) There exists a `secrets` folder.
