from unittest.mock import patch
import joblib

import pytest

from src.validate import ModelValidator


@pytest.fixture
def model_pipeline(test_config):
    return joblib.load(filename=f"{test_config.RESOURCES_FOLDER}/model.pkl")


@pytest.fixture
def input_df(test_config):
    return joblib.load(f"{test_config.RESOURCES_FOLDER}/preprocessed_data.pkl")


def test_get_metrics(test_config, input_df, model_pipeline):
    mv = ModelValidator(test_config, input_df, model_pipeline)
    metrics = mv.get_metrics()

    assert metrics is not None


@patch("matplotlib.pyplot.show")
def test_plot(
    mock_plot, test_config, input_df, model_pipeline
):  # pylint: disable=unused-argument
    mv = ModelValidator(test_config, input_df, model_pipeline)
    plt = mv.plot_hist_vs_pred()

    plt.savefig(fname=f"{test_config.RESOURCES_FOLDER}/plot_hist_vs_pred.png")
