import json

from src.configuration import Config
from src.preprocess import DataPreprocessor
from src.split import DataSplitter
from src.train import ModelTrainer
from src.validate import ModelValidator
from src.score import Scorer


def main():
    # read in data for building the model
    input_path = "../data/train_input.json"
    with open(input_path, "r", encoding="utf-8") as input_file:
        input_data = json.load(input_file)

    # preprocess
    preprocessor = DataPreprocessor(Config, input_data)
    data = preprocessor.preprocess()

    # split train test
    splitter = DataSplitter(Config, data)
    df_train, df_test = splitter.split(split_ratio=0.8)

    # train a model
    trainer = ModelTrainer(Config, df_train)
    model_pipeline = trainer.train_model()

    # validate performance
    validator = ModelValidator(Config, data, model_pipeline)
    metrics_dict = validator.get_metrics()
    print(f"the metrics are: \n {metrics_dict}")

    plt = validator.plot_hist_vs_pred()

    # score a prediction
    input_path = "../data/score_input.json"
    with open(input_path, "r", encoding="utf-8") as input_file:
        score_data = json.load(input_file)

    scorer = Scorer(Config, score_data, model_pipeline)
    feature_array = scorer.prepare_feature_array()

    score = scorer.get_prediction(feature_array)
    print(f"the prediction for the end balance for the given period is: {score[0]}")


if __name__ == "__main__":
    main()
