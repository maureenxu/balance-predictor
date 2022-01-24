import argparse
import os
import pickle

from src import split, utils
import configuration as config


def get_args():
    parser = argparse.ArgumentParser(
        prog="data_splitor",
        description="select the defined tier of data, split to train and test"
    )
    parser.add_argument("--input-path", required=True, type=str)
    parser.add_argument("--split-ratio", required=True, type=float)
    parser.add_argument("--output-test-path", required=True, type=str)
    parser.add_argument("--output-train-path", required=True, type=str)

    args = parser.parse_args()

    return args


def main():
    args = get_args()

    input_path = os.path.join(args.input_path, config.INPUT_OUTPUT_FILENAMES["spliter"]["input"])

    with open(input_path, "rb") as input_file:
        df = pickle.load(input_file)

    spliter = split.DataSpliter(df, args.split_ratio)
    df_train, df_test = spliter.split()

    utils.pickle_dump_output(args.output_train_path, config.INPUT_OUTPUT_FILENAMES["spliter"]["output_train"], df_train)
    utils.pickle_dump_output(args.output_test_path, config.INPUT_OUTPUT_FILENAMES["spliter"]["output_test"], df_test)


if __name__ == "__main__":
    main()
