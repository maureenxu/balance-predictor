from unittest.mock import patch
import matplotlib.pyplot as plt
import joblib
import pytest
import pandas as pd

from src.validate import ModelValidator
import src.configuration as config


PATH = "../data/model.pkl"
MODEL_PIPELINE = joblib.load(filename=PATH)

INPUT_DF = joblib.load("../data/preprocessed_data.pkl")


def test_get_metrics():
    mv = ModelValidator(INPUT_DF, MODEL_PIPELINE)
    metrics = mv.get_metrics()

    assert metrics is not None


@patch("matplotlib.pyplot.show")
def test_plot(mock_show):
    mv = ModelValidator(INPUT_DF, MODEL_PIPELINE)
    plt = mv.plot_hist_vs_pred()

    plt.savefig(fname="../data/plot_hist_vs_pred.png")
