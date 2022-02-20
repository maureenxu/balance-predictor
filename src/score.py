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
        for i in range(self.config.SHIFT_NUM + 1):
            df_add_shift_diff.loc[:, self.config.TARGET + "_lag" + str(i + 1)] = \
                df_add_shift_diff.loc[:, self.config.TARGET].shift(i + 1)

            df_add_shift_diff.loc[:, self.config.TARGET + "_diff" + str(i + 1)] = \
                df_add_shift_diff.loc[:, self.config.TARGET + "_lag" + str(i + 1)].diff()

        scoring_feature_array = df_add_shift_diff.drop([self.config.TARGET], axis=1).iloc[-1].values

        return scoring_feature_array

    def get_prediction(self, scoring_feature_array: np.ndarray) -> float:
        try:
            return self.model.predict(scoring_feature_array)
        except:
            return -1.0
