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

        self.X_test = self.df.drop([self.config.TARGET], axis=1)
        self.y_test = self.df.loc[:, self.config.TARGET]
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
