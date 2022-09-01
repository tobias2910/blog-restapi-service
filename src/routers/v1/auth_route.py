from src.db.base import get_session
from src.schemas.auth_schema import AuthSchema, AuthTokenSchema, RefreshSchema
from src.services.auth_service import auth_service
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

TAG_INFORMATION = {
    "name": "auth",
    "description": "This endpoint can be used to perform the authentication",
}

router = APIRouter(tags=[TAG_INFORMATION["name"]])


@router.post(
    "/login",
    summary="Conduct the authentication",
    description="Provide your email and password to obtain a token that can be used for secured endpoints.",
    status_code=status.HTTP_200_OK,
    response_model=AuthTokenSchema,
)
async def authentication(
    auth_data: AuthSchema,
    db_session: AsyncSession = Depends(get_session),
):
    auth_tokens = await auth_service.authenticate_user(
        auth_data.email, auth_data.password, db_session
    )

    return auth_tokens


@router.post(
    "/refresh",
    summary="Refresh a token",
    description="Provide your refresh token to receive a new authentication token",
    status_code=status.HTTP_200_OK,
    response_model=AuthTokenSchema,
)
async def refresh_token(
    refresh_token: RefreshSchema,
):
    auth_tokens = await auth_service.refresh_token(refresh_token.refresh_token)

    return auth_tokens
