import pytest
import logging.config

from app.config import get_config
from app.server import LOGGING_CONFIG


@pytest.fixture(autouse=True, scope="package")
def logging_config():
    logging.config.dictConfig(LOGGING_CONFIG)
    yield


@pytest.fixture
def config():
    return get_config()
