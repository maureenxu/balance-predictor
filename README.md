# balance-predictor
this is a project for building an MLOps pipeline for training a balace predictor model

# Setting up the project

If for some reason you are not able to run the `make venv` command, please make sure you have performed something similiar to the following steps:

```bash
pip install cython # Expected to be installed by some of our dependencies, but not implicitly installed.
pip install -e . # Editable, local install of the current code base
pip install -r requirements.txt
pip install -r requirements-dev.txt
```
# Running the pipeline

To run the pipeline, use the `run_pipeline.sh` command, it will perform the full pipeline and show the scores.

# Running the services using Docker
... TODO


# External Dependencies
```bash

# OpenSUSE
zypper addrepo https://download.opensuse.org/repositories/science/openSUSE_Tumbleweed/science.repo
zypper install lapack gcc-fortran gcc-c++ 
```

