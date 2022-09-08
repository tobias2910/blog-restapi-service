"""Auth services."""
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.auth_schema import AuthTokenSchema
from src.services.token_service import token_service
from src.services.user_service import user_service


class AuthService:
    """Provides services for the authentication against the API."""

    async def authenticate_user(self, mail: str, password: str, db_session: AsyncSession) -> AuthTokenSchema:
        """Authenticate the user.

        Conducts the authentication and provide the access tokens, in case the mail
        and password is correct.

        Args:
            mail (str): The mail address of the user.
            password (str): The password of the user.
            db_session (AsyncSession): The session for the DB.

        Raises:
            HTTPException: Raised in case the mail and / or password is invalid.
            HTTPException: Raised in case other issues occur during the authentication process.

        Returns:
            AuthTokenSchema: The ```Access``` and ```Refresh``` tokens.
        """
        try:
            user = await user_service.get_user(db_session, mail)

            if user is None or not user.verify_password(password):
                raise HTTPException(  # noqa: TC301
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid email and / or password",
                )
            else:
                access_tokens = token_service.generate_auth_tokens(user.email)

                return access_tokens
        except HTTPException:
            raise
        except BaseException:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ups... Something went wrong. Please try again later",
            ) from BaseException

    async def refresh_token(self, token: str) -> AuthTokenSchema:
        """Refresh the access token.

        Verifies whether the provided refresh token is valid and provides
        new auth tokens.

        Args:
            token (str): The refresh token to validate.

        Raises:
            HTTPException: The provided token is not valid.
            HTTPException: The refresh token expired.

        Returns:
            AuthTokenSchema: The ```Access``` and ```Refresh``` tokens.
        """
        try:
            decoded_token = token_service.decode_token(token)
            if decoded_token is None:
                raise HTTPException(  # noqa: TC301
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid refresh token",
                )
            else:
                access_tokens = token_service.generate_auth_tokens(decoded_token.sub)

                return access_tokens
        except HTTPException:
            raise
        except BaseException:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token expired",
            ) from BaseException


auth_service = AuthService()
