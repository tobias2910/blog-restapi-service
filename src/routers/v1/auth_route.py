"""All authentication related endpoints."""
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.base import get_session
from src.schemas.auth_schema import AuthSchema, AuthTokenSchema, RefreshSchema
from src.services.auth_service import auth_service

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
) -> AuthTokenSchema:
    """Endpoint for conducting the authentication.

    Args:
        auth_data (AuthSchema): JSON that contains the mail address and password of the user.
        db_session (AsyncSession, optional): The session for the DB that will
            automatically injected using the ```Depends```functionality of FastAPI.

    Returns:
        AuthTokenSchema: The new issued access and refresh tokens
    """
    auth_tokens = await auth_service.authenticate_user(auth_data.email, auth_data.password, db_session)

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
) -> AuthTokenSchema:
    """Endpoint to obtain a new access token based on a valid refresh token.

    Args:
        refresh_token (RefreshSchema): The refresh token to validated

    Returns:
        AuthTokenSchema: The new issued access and refresh tokens
    """
    auth_tokens = await auth_service.refresh_token(refresh_token.refresh_token)

    return auth_tokens
