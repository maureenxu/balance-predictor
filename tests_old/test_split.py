import pytest
import pandas as pd
import joblib

from src.split import DataSpliter
import src.configuration as config

INPUT_DF = joblib.load("../data/preprocessed_data.pkl")

# print(INPUT_DF.columns)
# print(INPUT_DF.dtypes)
print(INPUT_DF.head())

SPLIT_RATIO = 0.8


def test_assign_tiers():
    data_spliter = DataSpliter(INPUT_DF, SPLIT_RATIO)
    result = data_spliter.df.shape

    expected = (616, 43)

    assert result == expected


def test_split():
    data_spliter = DataSpliter(INPUT_DF, SPLIT_RATIO)
    df_train_result, df_test_result = data_spliter.split()

    expected_train_shape = (493, 43)
    expected_test_shape = (123, 43)

    assert df_train_result.shape == expected_train_shape
    assert df_test_result.shape == expected_test_shape
