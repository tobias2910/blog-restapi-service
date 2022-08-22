from app.config.settings import settings
from fastapi.testclient import TestClient

from app.schemas.token_schema import Auth_Token


def get_auth_token_header(client: TestClient) -> Auth_Token:
    credentials = {"email": settings.ADMIN_USER, "password": settings.ADMIN_PW}

    response = client.post(f"{settings.API_PATH}/auth/", json=credentials)
    auth_tokens = response.json()
    access_token = auth_tokens["access_token"]["token"]
    header = {"Authorization": f"Bearer {access_token}"}
    return header
