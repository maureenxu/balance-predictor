from datetime import timedelta

import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
import src.utils as ut

from src.configuration import Config


class Scorer:
    def __init__(self, config: Config, data: list, model: Pipeline):
        self.config = config

        # convert json object to dataframe
        self.data = data
        self.df = self._convert_json_to_df()

        # parse datetime string to a datetime object
        self.df[config.DT_OBJ] = self.df[self.config.BOOKING_DT].apply(
            ut.parse_dt_string
        )

        self.model = model

    def _convert_json_to_df(self) -> pd.DataFrame:
        flat_j_obj = []

        for item in self.data:
            flat_item = ut.flatten_json(item)
            flat_j_obj.append(flat_item)

        df = pd.DataFrame.from_records(flat_j_obj)
        df.reset_index(drop=True, inplace=True)

        return df

    def prepare_feature_array(self) -> np.ndarray:
        self.df.sort_values(by=self.config.DT_OBJ, ascending=True, inplace=True)

        self.df["balanceAfterBooking_value"] = self.df[
            "balanceAfterBooking_value"
        ].astype(float)
        self.df[self.config.TARGET] = self.df.apply(
            lambda x: ut.correct_credit_debt(
                x["balanceAfterBooking_creditDebitIndicator"],
                x["balanceAfterBooking_value"],
            ),
            axis=1,
        )

        df_agg = self.df.groupby(
            pd.Grouper(key=self.config.DT_OBJ, freq=self.config.AGG_BY)
        )[self.config.TARGET].sum()
        df_agg = pd.DataFrame(df_agg)

        # shift and calculate diffs
        df_add_shift_diff = df_agg.copy()

        # add one more row with last date + 1 day
        last_date = df_add_shift_diff.index[-1]
        next_date = last_date + timedelta(days=1)
        df_add_shift_diff.loc[next_date] = np.nan

        for i in range(self.config.SHIFT_NUM):
            df_add_shift_diff.loc[
                :, self.config.TARGET + "_lag" + str(i + 1)
            ] = df_add_shift_diff.loc[:, self.config.TARGET].shift(i + 1)

            df_add_shift_diff.loc[
                :, self.config.TARGET + "_diff" + str(i + 1)
            ] = df_add_shift_diff.loc[
                :, self.config.TARGET + "_lag" + str(i + 1)
            ].diff()

        scoring_feature_array = (
            df_add_shift_diff.drop([self.config.TARGET], axis=1).iloc[-1].values
        )

        return scoring_feature_array

    def get_prediction(self, scoring_feature_array: np.ndarray) -> float:
        try:
            score = self.model.predict([scoring_feature_array])
            return score
        # pylint: disable=broad-except
        except Exception as e:
            print(f"exception {e}")
            return -1.0


# if __name__=="__main__":
#     import json
#     from configuration import Config
#
#     input_path = "../data/input.json"
#     with open(input_path) as input_file:
#         data = json.load(input_file)
#
#     with open("../data/model_pipeline.pickle", "rb") as file:
#         model_pipeline = pickle.load(file)
#
#     scorer = Scorer(Config, data, model_pipeline)
#     feature_array = scorer.prepare_feature_array()
#
#     score = scorer.get_prediction(feature_array)
#     print(score)
