import pandas as pd
from matplotlib import pyplot as plt
from sklearn.model_selection import TimeSeriesSplit, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler

import configuration as config
import src.utils as ut


class ModelValidator:
    def __init__(self, df_test: pd.DataFrame, model_pipeline):
        self.df = df_test
        self.model_pipeline = model_pipeline

        self.X_test = self.df.drop([config.TARGET], axis=1)
        self.y_test = self.df.loc[:, config.TARGET]
        self.y_pred = self.model_pipeline.predict(self.X_test)

    def get_metrics(self):
        metrics_dict = ut.regression_results(self.y_test, self.y_pred)

        return metrics_dict

    def plot_hist_vs_pred(self):
        self.df.loc[:, config.TARGET + "_pred"] = self.y_pred
        plt.plot(self.df[config.TARGET], "b")
        plt.plot(self.df[config.TARGET + "_pred"], "r")
        plt.legend(["History", "Prediction"])
        plt.show()

        return plt
