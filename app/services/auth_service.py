from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.user_service import user_service
from app.services.token_service import token_service

from app.schemas.auth_schema import AuthTokenSchema


class Auth_service:
    """
    Provides services for the authentication against the API
    """

    async def authenticate_user(
        self, mail: str, password: str, db_session: AsyncSession
    ) -> AuthTokenSchema:
        """
        Conducts the authentication and provide the access tokens, in case the mail
        and password is correct.
        """
        try:
            user = await user_service.get_user(db_session, mail)

            if user is None or not user.verify_password(password):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid email and / or password",
                )

            access_tokens = token_service.generate_auth_tokens(user.email)

            return access_tokens
        except HTTPException as e:
            raise (e)
        except:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ups... Something went wrong. Please try again later",
            )

    async def refresh_token(self, token: str) -> AuthTokenSchema:
        """
        Verifies whether the provided refresh token is valid and provides
        new auth tokens in case they are
        """
        try:
            decoded_token = token_service.decode_token(token)
            if decoded_token is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid refresh token",
                )
            access_tokens = token_service.generate_auth_tokens(decoded_token.sub)

            return access_tokens
        except:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token expired",
            )


auth_service = Auth_service()
