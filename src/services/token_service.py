"""Token services."""
from datetime import datetime, timedelta

from jose import jwt
from jose.exceptions import ExpiredSignatureError

from src.config.settings import settings
from src.schemas.token_schema import AuthToken, Token, TokenPayload, TokenTypes


class TokenService:
    """Provides services for generating the auth tokens."""

    def __generate_token(
        self,
        user_id: str,
        expires_in: int,
        type: TokenTypes,
        secret: str = settings.JWT_SECRET_KEY,
    ) -> str:
        """Generate a new JWT token.

        Args:
            user_id (str): The mail address of the user to use as a ```sub``` in the token.
            expires_in (int): The UNIX timestamp indicating the expire time of the token.
            type (TokenTypes): The type of token.
            secret (str, optional): The algorithm to use for encoding the token.

        Returns:
            str: An encoded JWT token.
        """
        payload = {
            "sub": user_id,
            "iat": int(datetime.now().timestamp()),
            "exp": expires_in,
            "type": type,
        }

        return jwt.encode(payload, secret, algorithm=settings.ALGORITHM)  # type: ignore[no-any-return]

    def generate_auth_tokens(self, user_id: str) -> AuthToken:
        """Generate the access and refresh tokens.

        Args:
            user_id (str): The mail address of the user that will be used as a ```sub``` in the token.

        Returns:
            AuthToken: The auth object containing an ```access``` and ```refresh```token.
        """
        access_token_expire = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_token_expire = datetime.now() + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)

        access_token = self.__generate_token(
            user_id, int(access_token_expire.timestamp()), TokenTypes.ACCESS_TOKEN
        )
        refresh_token = self.__generate_token(
            user_id,
            int(refresh_token_expire.timestamp()),
            TokenTypes.REFRESH_TOKEN,
            settings.JWT_REFRESH_SECRET_KEY,
        )

        auth_token = AuthToken(
            __root__={
                TokenTypes.ACCESS_TOKEN: Token(token=access_token, expires=access_token_expire),
                TokenTypes.REFRESH_TOKEN.value: Token(token=refresh_token, expires=refresh_token_expire),
            }
        )

        return auth_token.dict()["__root__"]

    def decode_token(self, token: str) -> TokenPayload:
        """Decode the provided JWT token and returns it.

        Args:
            token (str): The JWT token that shall be validated and encoded.

        Raises:
            Exception: General exception that needs to be handled from the calling function.

        Returns:
            TokenPayload: The decoded JWT token.
        """
        try:
            token_payload = jwt.decode(token, settings.JWT_SECRET_KEY, settings.ALGORITHM)

            return TokenPayload(**token_payload)  # noqa: TC300
        except ExpiredSignatureError:
            raise Exception() from ExpiredSignatureError  # noqa: TC002


token_service = TokenService()
