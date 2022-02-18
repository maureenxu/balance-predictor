import pandas as pd
from sklearn.model_selection import TimeSeriesSplit, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler

from src.configuration import Config


class ModelTrainer:
    def __init__(self, config: Config, df_train: pd.DataFrame, params: dict):
        self.df = df_train
        self.config = config
        self.model = self.config.MODEL.set_params(**params)
        self.model_pipeline = Pipeline(
            steps=[("scaler", MinMaxScaler()), ("model", self.model)]
        )

        self.X_train = self.df.drop([self.config.TARGET], axis=1).values
        self.y_train = self.df.loc[:, self.config.TARGET].values

    def cross_validate(self):
        tscv = TimeSeriesSplit(n_splits=3)
        cv_results = cross_val_score(
            self.model_pipeline,
            self.X_train,
            self.y_train,
            cv=tscv,
            n_jobs=-1,
            scoring="r2",
        )

        return cv_results

    def train_model(self):
        self.model_pipeline.fit(self.X_train, self.y_train)

        return self.model_pipeline


# if __name__=="__main__":
#     import json
#     import pickle
#     from configuration import Config
#
#     input_path = "../data/training_data.pickle"
#     with open(input_path, "rb") as input_file:
#         data = pickle.load(input_file)
#
#     trainer = ModelTrainer(Config, data, Config.PARAMS)
#     model_pipeline = trainer.train_model()
#
#     output_path = "../data/model_pipeline.pickle"
#     with open(output_path, "wb") as file:
#         pickle.dump(model_pipeline, file)
