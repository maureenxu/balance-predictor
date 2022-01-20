import argparse
import json
import pickle
from pathlib import Path

from src.preprocess import DataPreprocessor as dp
import configuration as config


def get_args():
    args = argparse.ArgumentParser(
        prog="data_preprocessor",
        description="preprocess input data to prepare for the training"
    )
    args.add_argument("--input-path", required=True, type=str)
    args.add_argument("--output-path", required=True, type=str)

    return args


def main():
    args = get_args()

    input_path = Path(args.input_path) / config.INPUT_OUTPUT_FILENAMES["preprocessor"]["input"]
    with open(input_path) as input_file:
        data = json.load(input_file)

    preprocessor = dp(data)
    df_output = preprocessor.preprocess()

    output_path = Path(args.output_path).mkdir(parents=True, exist_ok=True) / config.INPUT_OUTPUT_FILENAMES["preprocessor"]["output"]

    with open(output_path) as output_file:
        pickle.dump(df_output, output_file)


if "__name__" == "__main__":
    main()