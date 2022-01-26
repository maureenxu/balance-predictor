import json

import pytest

from src.preprocess import DataPreprocessor


def test_initialisation(test_config, input_data):
    data_preprocessor = DataPreprocessor(test_config, input_data)
    result = data_preprocessor.df.shape

    expected = (7166, 8)

    assert result == expected


def test_preprocess(test_config, input_data):
    data_preprocessor = DataPreprocessor(test_config, input_data)
    df = data_preprocessor.preprocess()

    result = df.shape

    expected = (686, 43)

    # persist the file for further tests
    # joblib.dump(value=df,
    #             filename="../data/preprocessed_data.pkl")

    assert df is not None
    assert result == expected
