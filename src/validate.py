import pandas as pd
from matplotlib import pyplot as plt
from sklearn.pipeline import Pipeline


import src.utils as ut
from src.configuration import Config


class ModelValidator:
    def __init__(self, config: Config, df_test: pd.DataFrame, model_pipeline: Pipeline):
        self.df = df_test
        self.model_pipeline = model_pipeline
        self.config = config

        self.X_test = self.df.drop([self.config.TARGET], axis=1).values
        self.y_test = self.df.loc[:, self.config.TARGET].values
        self.y_pred = self.model_pipeline.predict(self.X_test)

    def get_metrics(self):
        metrics_dict = ut.regression_results(self.y_test, self.y_pred)

        return metrics_dict

    def plot_hist_vs_pred(self):
        self.df.loc[:, self.config.TARGET + "_pred"] = self.y_pred
        plt.plot(self.df[self.config.TARGET], "b")
        plt.plot(self.df[self.config.TARGET + "_pred"], "r")
        plt.legend(["History", "Prediction"])
        plt.show()

        return plt


# if __name__=="__main__":
#     import json
#     import pickle
#     from configuration import Config
#
#     input_path = "../data/testing_data.pickle"
#     with open(input_path, "rb") as input_file:
#         data = pickle.load(input_file)
#
#     with open("../data/model_pipeline.pickle", "rb") as file:
#         model_pipeline = pickle.load(file)
#
#     validator = ModelValidator(Config, data, model_pipeline)
#
#     metrics_dict = validator.get_metrics()
#     plt = validator.plot_hist_vs_pred()
