import argparse
import pickle
from pathlib import Path

from src.train import ModelTrainer as mt
import configuration as config


def get_args():
    args = argparse.ArgumentParser(
        prog="data_splitor",
        description="select the defined tier of data, split to train and test"
    )
    args.add_argument("--input-path", required=True, type=str)
    args.add_argument("--output-path", required=True, type=str)

    return args


def main():
    args = get_args()

    input_path = Path(args.input_path) / config.INPUT_OUTPUT_FILENAMES["trainer"]["input"]
    with open(input_path) as input_file:
        df = pickle.load(input_file)

    trainer = mt(df, config.PARAMS)
    cv_results = trainer.cross_validate()
    model_pipeline = trainer.train_model()

    print(f"the cross validation results are: {cv_results}")

    output_path = Path(args.output_path).mkdir(parents=True, exist_ok=True) / config.INPUT_OUTPUT_FILENAMES["trainer"]["output"]

    with open(output_path) as output_file:
        pickle.dump(model_pipeline, output_file)


if "__name__" == "__main__":
    main()