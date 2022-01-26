import pytest
import joblib

from src.split import DataSpliter


@pytest.fixture
def input_df(test_config):
    return joblib.load(f"{test_config.RESOURCES_FOLDER}/preprocessed_data.pkl")


SPLIT_RATIO = 0.8

# TODO: Add tests for remaining config settings.


def test_assign_tiers(test_config, input_df):
    data_spliter = DataSpliter(test_config, input_df, SPLIT_RATIO)
    result = data_spliter.df.shape

    expected = (616, 43)

    assert result == expected


def test_split(test_config, input_df):
    data_spliter = DataSpliter(test_config, input_df, SPLIT_RATIO)
    df_train_result, df_test_result = data_spliter.split()

    expected_train_shape = (493, 43)
    expected_test_shape = (123, 43)

    assert df_train_result.shape == expected_train_shape
    assert df_test_result.shape == expected_test_shape
