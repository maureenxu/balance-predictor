import pandas as pd
from sklearn.model_selection import TimeSeriesSplit, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler

import configuration as config


class ModelTrainer:
    def __init__(self, df_train: pd.DataFrame, params: dict):
        self.df = df_train
        self.model = config.MODEL.set_params(**params)
        self.model_pipeline = Pipeline(steps=[('scaler', MinMaxScaler()), ('model', self.model)])

        self.X_train = self.df.drop([config.TARGET], axis=1)
        self.y_train = self.df.loc[:, config.TARGET]

    def cross_validate(self):
        tscv = TimeSeriesSplit(n_splits=3)
        cv_results = cross_val_score(self.model_pipeline, self.X_train, self.y_train, cv=tscv, n_jobs=-1, scoring="r2")

        return cv_results

    def train_model(self):
        self.model_pipeline.fit(self.X_train, self.y_train)

        return self.model_pipeline