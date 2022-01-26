import argparse
import os
import pickle

from src import train, utils
import src.configuration as config


def get_args():
    parser = argparse.ArgumentParser(
        prog="model_trainer",
        description="train a model"
    )
    parser.add_argument("--input-path", required=True, type=str)
    parser.add_argument("--output-path", required=True, type=str)

    args = parser.parse_args()

    return args


def main():
    args = get_args()

    input_path = os.path.join(args.input_path, config.INPUT_OUTPUT_FILENAMES["trainer"]["input"])

    with open(input_path, "rb") as input_file:
        df = pickle.load(input_file)

    trainer = train.ModelTrainer(df, config.PARAMS)
    cv_results = trainer.cross_validate()
    model_pipeline = trainer.train_model()

    print(f"the cross validation results are: {cv_results}")

    utils.pickle_dump_output(args.output_path, config.INPUT_OUTPUT_FILENAMES["trainer"]["output"], model_pipeline)


if __name__ == "__main__":
    main()
