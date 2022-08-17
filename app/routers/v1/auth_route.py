from fastapi import APIRouter, status

from app.services.auth_service import auth_service
from app.schemas.auth_schema import Auth_schema

# from app.schemas.token_schema import Auth_Token

TAG_INFORMATION = {
    "name": "auth",
    "description": "This endpoint can be used to perform the authentication",
}

router = APIRouter(tags=[TAG_INFORMATION["name"]])


@router.post(
    "/",
    summary="Conduct the authentication",
    description="Provide your email and password to receive a token that can be used for all secured endpoints.",
    status_code=status.HTTP_200_OK,
    # response_model=Auth_Token
)
async def authentication(auth_data: Auth_schema):
    auth_tokens = await auth_service.authenticate_user(
        auth_data.email, auth_data.password
    )
    return auth_tokens
