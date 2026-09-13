import os

import pytest


@pytest.fixture(scope="session", autouse=True)
def configure_test_database():
    variables = {
        "POSTGRES_HOST": "localhost",
        "POSTGRES_PORT": "5433",
        "POSTGRES_DB": "houblon_test",
        "POSTGRES_USER": "test",
        "POSTGRES_PASSWORD": "test",
    }

    old_values = {}

    for key, value in variables.items():
        old_values[key] = os.environ.get(key)
        os.environ[key] = value

    yield

    for key, old_value in old_values.items():
        if old_value is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = old_value
