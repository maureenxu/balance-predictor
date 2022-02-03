import datetime
import json
from multiprocessing.sharedctypes import Value
import os

import pandas as pd
from pathlib import Path

import pytest

import src.utils as ut


def test_flatten_dict_identity():
    sample_dict = {"a": 1, "b": 2, "c": 3}
    assert ut.flatten_json(sample_dict) == sample_dict


def test_flatten_dict_depth_1():
    sample_dict = {"a": {"a1": 1, "a2": 2}, "b": 1, "c": {"c1": 1, "c2": 2}}
    assert ut.flatten_json(sample_dict) == {
        "a_a1": 1,
        "a_a2": 2,
        "b": 1,
        "c_c1": 1,
        "c_c2": 2,
    }


def test_flatten_dict_vardepth():
    sample_dict = {
        "a": {"a1": 1, "a2": {"i": {"A": {"1": 1}}}},
        "b": 1,
        "c": {"c1": 1, "c2": 2},
    }
    assert ut.flatten_json(sample_dict) == {
        "a_a1": 1,
        "a_a2_i_A_1": 1,
        "b": 1,
        "c_c1": 1,
        "c_c2": 2,
    }


def test_flatten_dict_from_string():
    with pytest.raises(ValueError):
        ut.flatten_json("This is a random string, or not")


# def test_flatten_json(test_config):
#     with open(f"{test_config.RESOURCES_FOLDER}/input.json", encoding="utf8") as j:
#         j_obj = json.load(j)

#     result = []

#     for item in j_obj:
#         flat_item = ut.flatten_json(item)
#         result.append(flat_item)

#     result_len = len(result)
#     expected_len = len(j_obj)

#     assert result is not None
#     assert result_len == expected_len


def test_parse_dt_string():
    """
    Test the datetime utility of converting our datetime string formats
    to datetime objects. The utility should ignore data after the 12th
    character.

    Expected (possible) conversion:
    20201209185334801472 -> 2020-12-09T18:53:00
    """
    dt_string = "20201209185334801472"
    result = ut.parse_dt_string(dt_string)

    assert result is not None
    assert isinstance(result, datetime.datetime)
    assert "2020-12-09T18:53:00" == result.strftime("%Y-%m-%dT%H:%M:%S")


def test_correct_credit_debt():
    amount = 100

    assert -100 == ut.correct_credit_debt("D", amount)
    assert 100 == ut.correct_credit_debt("C", amount)


def test_incorrect_indicator():
    amount = 100

    # By default we assume it is about credit, instead of debt
    assert 100 == ut.correct_credit_debt("AAA", amount)


def test_add_shift_and_diff(test_config, sample_dataframe):
    # The code this test is about:
    df_add_shift_diff = ut.add_shift_and_diff(sample_dataframe, test_config.TARGET, 1)

    # The assertions:
    assert df_add_shift_diff is not None
    assert df_add_shift_diff.equals(
        pd.DataFrame(
            data={
                "date": [datetime.date(2019, 1, 4)],
                "balanceAfterBooking_value_corr": [1679.86],
                "balanceAfterBooking_value_corr_lag1": [7672.09],
                "balanceAfterBooking_value_corr_diff1": [-13250.96],
            },
            index=[2],
        )
    )


def test_pickle_dump_output(test_config):
    obj_test = {"a": 1, "b": 2}

    output_path = f"{test_config.RESOURCES_FOLDER}/data"
    file_name = "test_pickle"

    ut.pickle_dump_output(output_path, file_name, obj_test)

    output_file_path = Path(os.path.join(output_path, file_name))
    assert output_file_path.is_file()
