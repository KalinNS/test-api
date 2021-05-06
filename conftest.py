import pytest

from api.client import BearClient

@pytest.fixture(scope="session")
def client():
    client = BearClient("http://localhost:8091")
    return client

