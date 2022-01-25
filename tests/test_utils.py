import datetime
import json
import os

import pandas as pd
from pathlib import Path

import src.utils as ut


def test_flatten_json(test_config):
    with open(f"{test_config.RESOURCES_FOLDER}/input.json", encoding="utf8") as j:
        j_obj = json.load(j)

    result = []

    for item in j_obj:
        flat_item = ut.flatten_json(item)
        result.append(flat_item)

    result_len = len(result)
    expected_len = len(j_obj)

    assert result is not None
    assert result_len == expected_len


def test_parse_dt_string():
    dt_string = "20201209185334801472"
    result = ut.parse_dt_string(dt_string)

    assert result is not None
    assert type(result) is datetime.datetime


def test_correct_credit_debt():
    cd_indicator1 = "D"
    cd_indicator2 = "C"

    amount = 100

    result1 = ut.correct_credit_debt(cd_indicator1, amount)
    result2 = ut.correct_credit_debt(cd_indicator2, amount)

    expected1 = 0 - amount
    expected2 = amount

    assert result1 == expected1
    assert result2 == expected2


def test_add_shift_and_diff(test_config):
    with open(f"{test_config.RESOURCES_FOLDER}/input.json", encoding="utf8") as j:
        j_obj = json.load(j)

    flat_j_obj = []

    for item in j_obj:
        flat_item = ut.flatten_json(item)
        flat_j_obj.append(flat_item)

    df = pd.DataFrame.from_records(flat_j_obj)
    df.reset_index(drop=True, inplace=True)
    df[test_config.DT_OBJ] = df[test_config.BOOKING_DT].apply(ut.parse_dt_string)

    df.sort_values(by=test_config.DT_OBJ, ascending=True, inplace=True)

    df["balanceAfterBooking_value"] = df["balanceAfterBooking_value"].astype(float)
    df[test_config.TARGET] = df.apply(
        lambda x: ut.correct_credit_debt(
            x["balanceAfterBooking_creditDebitIndicator"],
            x["balanceAfterBooking_value"],
        ),
        axis=1,
    )

    df_agg = df.groupby(pd.Grouper(key=test_config.DT_OBJ, freq=test_config.AGG_BY))[
        test_config.TARGET
    ].sum()
    df_agg = pd.DataFrame(df_agg)

    df_add_shift_diff = ut.add_shift_and_diff(
        df_agg, test_config.TARGET, test_config.SHIFT_NUM
    )

    assert df_add_shift_diff is not None
    assert df_add_shift_diff.shape == (686, 43)


def test_pickle_dump_output(test_config):
    obj_test = {"a": 1, "b": 2}

    output_path = f"{test_config.RESOURCES_FOLDER}/data"
    file_name = "test_pickle"

    ut.pickle_dump_output(output_path, file_name, obj_test)

    output_file_path = Path(os.path.join(output_path, file_name))
    assert output_file_path.is_file()
