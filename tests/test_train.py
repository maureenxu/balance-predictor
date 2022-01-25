import joblib
import pytest

from src.train import ModelTrainer


@pytest.fixture
def input_df(test_config):
    return joblib.load(f"{test_config.RESOURCES_FOLDER}/preprocessed_data.pkl")


PARAMS = {"n_estimators": 50, "max_depth": 3, "min_impurity_decrease": 0}


def test_initialisation(test_config, input_df):
    mt = ModelTrainer(test_config, input_df, PARAMS)

    result_X = mt.X_train.shape
    result_y = mt.y_train.shape

    expected_X = (686, 42)
    expected_y = (686,)

    assert result_X == expected_X
    assert result_y == expected_y


def test_cross_validate(test_config, input_df):
    mt = ModelTrainer(test_config, input_df, PARAMS)
    cv_results = mt.cross_validate()

    assert cv_results is not None


def test_train_model(test_config, input_df):
    mt = ModelTrainer(test_config, input_df, PARAMS)
    model_pipeline = mt.train_model()

    assert model_pipeline is not None

    # persist model for later tests
    # model_file_name = "../data/model.pkl"
    # joblib.dump(value=model_pipeline, filename=model_file_name)
