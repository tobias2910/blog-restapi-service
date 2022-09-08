from typing import Dict

from httpx import AsyncClient

from src.config.settings import settings


async def get_auth_token_header(client: AsyncClient) -> Dict[str, str]:
    credentials = {"email": settings.ADMIN_USER, "password": settings.ADMIN_PW}

    response = await client.post(f"{settings.API_PATH}/auth/", json=credentials)
    auth_tokens = response.json()
    access_token = auth_tokens["access_token"]["token"]
    header = {"Authorization": f"Bearer {access_token}"}
    return header
