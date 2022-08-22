import pytest
from fastapi.testclient import TestClient

from app.db.base import get_session
from app.app import app
from tests.utils.utils import get_auth_token_header

# Arrange
@pytest.fixture(scope="session")
def db_session():
    yield get_session()


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="module")
def auth_header(client: TestClient):
    return get_auth_token_header(client)
