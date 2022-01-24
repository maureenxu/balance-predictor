import argparse
import json
import os

from src import preprocess, utils
import configuration as config


def get_args():
    parser = argparse.ArgumentParser(
        prog="data_preprocessor",
        description="preprocess input data to prepare for the training"
    )
    parser.add_argument("--input-path", required=True, type=str)
    parser.add_argument("--output-path", required=True, type=str)

    args = parser.parse_args()

    return args


def main():
    args = get_args()

    input_path = os.path.join(args.input_path, config.INPUT_OUTPUT_FILENAMES["preprocessor"]["input"])
    with open(input_path) as input_file:
        data = json.load(input_file)

    preprocessor = preprocess.DataPreprocessor(data)
    df_output = preprocessor.preprocess()

    utils.pickle_dump_output(args.output_path, config.INPUT_OUTPUT_FILENAMES["preprocessor"]["output"], df_output)


if __name__ == "__main__":
    main()
