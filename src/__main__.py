import json

from configuration import Config
from preprocess import DataPreprocessor
from split import DataSplitter
from train import ModelTrainer
from validate import ModelValidator
from score import Scorer

def main():
    # read in data for building the model
    input_path = "../data/train_input.json"
    with open(input_path, "r", encoding="utf-8") as input_file:
        input_data = json.load(input_file)

    # preprocess
    preprocessor = DataPreprocessor(Config, input_data)
    data = preprocessor.preprocess()

    # split train test
    df_train, df_test = DataSplitter.split(Config, data)

    # train a model
    trainer = ModelTrainer(Config, df_train)
    model_pipeline = trainer.train_model()

    # validate performance
    validator = ModelValidator(Config, data, model_pipeline)
    metrics_dict = validator.get_metrics()
    print(f"the metrics are: \n {metrics_dict}")

    plt = validator.plot_hist_vs_pred()
    plt.show()

    # score a prediction
    input_path = "../data/score_input.json"
    with open(input_path, "r", encoding="utf-8") as input_file:
        score_data = json.load(input_file)

    scorer = Scorer(Config, score_data, model_pipeline)
    feature_array = scorer.prepare_feature_array()

    score = scorer.get_prediction(feature_array)
    print(score)

if __name__ == "__main__":
    main()
