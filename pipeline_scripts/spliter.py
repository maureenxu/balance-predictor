import argparse
import pickle
from pathlib import Path

from src.split import DataSpliter as ds
import configuration as config


def get_args():
    args = argparse.ArgumentParser(
        prog="data_splitor",
        description="select the defined tier of data, split to train and test"
    )
    args.add_argument("--input-path", required=True, type=str)
    args.add_argument("--split-ratio", required=True, type=float)
    args.add_argument("--output-test-path", required=True, type=str)
    args.add_argument("--output-train-path", required=True, type=str)

    return args


def main():
    args = get_args()

    input_path = Path(args.input_path) / config.INPUT_OUTPUT_FILENAMES["spliter"]["input"]
    with open(input_path) as input_file:
        df = pickle.load(input_file)

    spliter = ds(df, args.split_ratio)
    df_train, df_test = spliter.split()

    output_train_path = Path(args.output_train_path).mkdir(parents=True, exist_ok=True) / config.INPUT_OUTPUT_FILENAMES["spliter"]["output_train"]
    output_test_path = Path(args.output_test_path).mkdir(parents=True, exist_ok=True) / config.INPUT_OUTPUT_FILENAMES["spliter"]["output_test"]

    with open(output_train_path) as output_file:
        pickle.dump(df_train, output_file)
    
    with open(output_test_path) as output_file:
        pickle.dump(df_test, output_file)


if "__name__" == "__main__":
    main()