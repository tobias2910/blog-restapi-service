from typing import Dict

from fastapi import status
from fastapi.testclient import TestClient

from app.config.settings import settings


def test_valid_token(client: TestClient, auth_header: Dict[str, str]) -> None:
    response = client.get(f"{settings.API_PATH}/articles/", headers=auth_header)
    assert response.status_code == status.HTTP_200_OK


def test_invalid_token(client: TestClient) -> None:
    response = client.get(f"{settings.API_PATH}/articles/")
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_get_article(client: TestClient, auth_header: Dict[str, str]) -> None:
    response = client.get(f"{settings.API_PATH}/articles/52", headers=auth_header)
    article = response.json()
    assert article["author"] == "Tobias Caliskan"
