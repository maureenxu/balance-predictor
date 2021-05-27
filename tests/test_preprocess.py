import json
import joblib

from src.preprocess import DataPreprocessor


with open('../data/0b24be9f1c36838864.json', encoding='utf8') as j:
    INPUT_DATA = json.load(j)


def test_initialisation():
    data_preprocessor = DataPreprocessor(INPUT_DATA)
    result = data_preprocessor.df.shape

    expected = (7166, 8)

    assert result == expected


def test_preprocess():
    data_preprocessor = DataPreprocessor(INPUT_DATA)
    df = data_preprocessor.preprocess()

    result = df.shape

    expected = (686, 43)

    # persist the file for further tests
    # joblib.dump(value=df,
    #             filename="../data/preprocessed_data.pkl")

    assert df is not None
    assert result == expected


