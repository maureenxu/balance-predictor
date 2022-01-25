import json

import pytest

from src.configuration import Config


@pytest.fixture
def test_config():
    Config.RESOURCES_FOLDER = f"data"
    return Config


@pytest.fixture
def input_data(test_config):
    with open(f"{test_config.RESOURCES_FOLDER}/input.json", encoding="utf8") as j:
        return json.load(j)
