import pandas as pd
import src.utils as ut

from src.configuration import Config


# pylint: disable=too-few-public-methods
class DataPreprocessor:
    def __init__(self, config: Config, data: list):
        self.config = config

        # convert json object to dataframe
        self.data = data
        self.df = self._convert_json_to_df()

        print(f"Input data shape: {self.df.shape}", end="\n")
        print(f"Input data columns: {self.df.columns}", end="\n")

        # parse datetime string to a datetime object
        self.df[config.DT_OBJ] = self.df[self.config.BOOKING_DT].apply(
            ut.parse_dt_string
        )

    def _convert_json_to_df(self) -> pd.DataFrame:
        flat_j_obj = []

        for item in self.data:
            flat_item = ut.flatten_json(item)
            flat_j_obj.append(flat_item)

        df = pd.DataFrame.from_records(flat_j_obj)
        df.reset_index(drop=True, inplace=True)

        return df

    def preprocess(self):
        try:
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

            df_add_shift_diff = ut.add_shift_and_diff(
                df_agg, self.config.TARGET, self.config.SHIFT_NUM
            )

            print(f"Output data shape: {df_add_shift_diff.shape}", end="\n")

            return df_add_shift_diff

        # pylint: disable=broad-except
        except Exception as e:
            print(f"Exception during data preprocessing: {e}", end="\n")

            return None
