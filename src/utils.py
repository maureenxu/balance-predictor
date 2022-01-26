import os
import datetime
import pickle

from dateutil.parser import parse

from sklearn import metrics
import numpy as np
import pandas as pd


def flatten_json(j_obj: dict) -> dict:
    output = {}

    if not isinstance(j_obj, (dict, list)):
        raise ValueError(f"Input is of unexpected type: {type(j_obj)}")

    def flatten(x, name=""):
        if isinstance(x, dict):
            for a in x:
                flatten(x[a], name + a + "_")
        elif isinstance(x, list):
            i = 0
            for a in x:
                flatten(a, name + str(i) + "_")
                i += 1
        else:
            output[name[:-1]] = x

    flatten(j_obj)

    return output


def parse_dt_string(dt_string: str) -> datetime.datetime:
    # See: https://docs.python.org/3/library/datetime.html
    #
    # Can simplify to: ignore after the 12th character, parse the remainder:
    # return datetime.datetime.strptime(dt_string[:12], '%Y%m%d%H%M')

    year = dt_string[:4]
    month = dt_string[4:6]
    day = dt_string[6:8]
    hour = dt_string[8:10]
    minute = dt_string[10:12]

    dt_obj = parse(year + "-" + month + "-" + day + " " + hour + ":" + minute)

    return dt_obj


def correct_credit_debt(cd_indicator: str, amount: float) -> float:
    if cd_indicator not in ["C", "D"]:
        # Would be good to explicitly mention alternative scenarios,
        # to share design choices with new engineers. It also provides
        # ways to manage when unexpected behavior occurs too often:
        cd_indicator = "C"
        print("Unknown CD_Indicator has occurred!")

    if cd_indicator == "D":
        amount = 0 - amount

    # ... by default we will assume it is about Credit, not Debt.
    return amount


def add_shift_and_diff(
    df: pd.DataFrame, amount_col: str, shift_num: int
) -> pd.DataFrame:
    new_df = df.copy()

    for i in range(shift_num):
        new_df.loc[:, amount_col + "_lag" + str(i + 1)] = df.loc[:, amount_col].shift(
            i + 1
        )
        new_df.loc[:, amount_col + "_diff" + str(i + 1)] = new_df.loc[
            :, amount_col + "_lag" + str(i + 1)
        ].diff()

    new_df.dropna(how="any", inplace=True)

    return new_df


def regression_results(y_true, y_pred):
    mae = metrics.mean_absolute_error(y_true, y_pred)
    mse = metrics.mean_squared_error(y_true, y_pred)
    mae_mean = mse / np.median(y_true)
    r2 = metrics.r2_score(y_true, y_pred)

    metrics_dict = {
        "r2": round(r2, 4),
        "MAE": round(mae, 4),
        "MSE": round(mse, 4),
        "MAE/Mean": round(mae_mean, 4),
        "RMSE": round(np.sqrt(mse), 4),
    }

    return metrics_dict


def pickle_dump_output(output_path, file_name, obj):

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    output_file_path = os.path.join(output_path, file_name)

    with open(output_file_path, "wb") as output_file:
        pickle.dump(obj, output_file)
