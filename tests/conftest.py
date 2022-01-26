import json
import datetime
import pandas as pd
import pytest

from src.configuration import Config

"""
@pytest.fixture
def sample_fixt():
    setUp()
    yield object_to_share_in_functions
    tearDown()
"""


@pytest.fixture
def test_config():
    Config.RESOURCES_FOLDER = f"data"
    return Config


@pytest.fixture
def input_data(test_config):
    with open(f"{test_config.RESOURCES_FOLDER}/input.json", encoding="utf8") as j:
        return json.load(j)


@pytest.fixture
def sample_dataframe():
    d = {
        "date": [
            datetime.date(2019, 1, 2),
            datetime.date(2019, 1, 3),
            datetime.date(2019, 1, 4),
        ],
        "balanceAfterBooking_value_corr": [
            20923.05,
            7672.09,
            1679.86,
        ],
    }
    df_agg = pd.DataFrame(data=d)
    return df_agg
