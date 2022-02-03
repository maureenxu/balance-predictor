import argparse
import os
import pickle

from src import validate, utils
import src.configuration as config


def get_args():
    parser = argparse.ArgumentParser(
        prog="model_validator",
        description="validate model performance"
    )
    parser.add_argument("--input-test-path", required=True, type=str)
    parser.add_argument("--input-model-path", required=True, type=str)
    parser.add_argument("--output-path", required=True, type=str)

    args = parser.parse_args()

    return args


def main():
    args = get_args()

    input_test_path = os.path.join(args.input_test_path, config.INPUT_OUTPUT_FILENAMES["validator"]["input_test"])
    input_model_path = os.path.join(args.input_model_path, config.INPUT_OUTPUT_FILENAMES["validator"]["input_model"])

    with open(input_test_path, "rb") as input_file:
        df = pickle.load(input_file)
    
    with open(input_model_path, "rb") as input_file:
        model_pipeline = pickle.load(input_file)

    validator = validate.ModelValidator(df, model_pipeline)
    metrics_dict = validator.get_metrics()
    plt = validator.plot_hist_vs_pred()

    print(f"the metrics are: {metrics_dict}")

    utils.pickle_dump_output(args.output_path, config.INPUT_OUTPUT_FILENAMES["validator"]["output_metrics"], metrics_dict)

    output_plot_path = os.path.join(args.output_path, config.INPUT_OUTPUT_FILENAMES["validator"]["output_plot"])
    plt.savefig(fname=output_plot_path)


if __name__ == "__main__":
    main()
