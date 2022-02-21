import pytest
import joblib

from src.split import DataSplitter


@pytest.fixture
def input_df(test_config):
    return joblib.load(f"{test_config.RESOURCES_FOLDER}/preprocessed_data.pkl")


SPLIT_RATIO = 0.8

# TODO: Add tests for remaining config settings.


def test_assign_tiers(test_config, input_df):
    data_spliter = DataSplitter(test_config, input_df)
    result = data_spliter.df.shape

    expected = (616, 43)

    assert result == expected


def test_split(test_config, input_df):
    data_spliter = DataSplitter(test_config, input_df)
    df_train_result, df_test_result = data_spliter.split(SPLIT_RATIO)

    expected_train_shape = (493, 43)
    expected_test_shape = (123, 43)

    assert df_train_result.shape == expected_train_shape
    assert df_test_result.shape == expected_test_shape
