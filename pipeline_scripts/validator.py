import argparse
import pickle
from pathlib import Path

from src.validate import ModelValidator as mv
import configuration as config


def get_args():
    args = argparse.ArgumentParser(
        prog="model_validator",
        description="validate model performance"
    )
    args.add_argument("--input-test-path", required=True, type=str)
    args.add_argument("--input-model-path", required=True, type=str)
    args.add_argument("--output-metrics-path", required=True, type=str)
    args.add_argument("--output-plot-path", required=True, type=str)

    return args


def main():
    args = get_args()

    input_test_path = Path(args.input_test_path) / config.INPUT_OUTPUT_FILENAMES["validator"]["input_test"]
    input_model_path = Path(args.input_model_path) / config.INPUT_OUTPUT_FILENAMES["validator"]["input_model"]

    with open(input_test_path) as input_file:
        df = pickle.load(input_file)
    
    with open(input_model_path) as input_file:
        model_pipeline = pickle.load(input_file)

    validator = mv(df, model_pipeline)
    metrics_dict = validator.get_metrics()
    plt = validator.plot_hist_vs_pred()

    print(f"the metrics are: {metrics_dict}")

    output_metrics_path = Path(args.output_metrics_path).mkdir(parents=True, exist_ok=True) / config.INPUT_OUTPUT_FILENAMES["validator"]["output_metrics"]
    output_plot_path = Path(args.output_plot_path).mkdir(parents=True, exist_ok=True) / config.INPUT_OUTPUT_FILENAMES["validator"]["output_plot"]

    with open(output_metrics_path) as output_file:
        pickle.dump(metrics_dict, output_file)
    
    plt.savefig(fname=output_plot_path)


if "__name__" == "__main__":
    main()