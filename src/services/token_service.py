from datetime import datetime, timedelta

from src.config.settings import settings
from src.schemas.token_schema import AuthToken, Token, TokenPayload, TokenTypes
from jose import jwt
from jose.exceptions import ExpiredSignatureError


class TokenService:
    """
    Provides services for generating the auth tokens used
    to get access to protected endpoints
    """

    def __generate_token(
        self,
        user_id: str,
        expires_in: int,
        type: TokenTypes,
        secret: str = settings.JWT_SECRET_KEY,
    ) -> str:
        """
        Generates a new JWT token
        """
        payload = {
            "sub": user_id,
            "iat": int(datetime.now().timestamp()),
            "exp": expires_in,
            "type": type,
        }

        return jwt.encode(payload, secret, algorithm=settings.ALGORITHM)

    def generate_auth_tokens(self, user_id: str) -> AuthToken:
        """
        Generates the access and refresh tokens
        """
        access_token_expire = datetime.now() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        refresh_token_expire = datetime.now() + timedelta(
            minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES
        )

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
                TokenTypes.ACCESS_TOKEN: Token(
                    token=access_token, expires=access_token_expire
                ),
                TokenTypes.REFRESH_TOKEN.value: Token(
                    token=refresh_token, expires=refresh_token_expire
                ),
            }
        )

        return auth_token.dict()["__root__"]

    def decode_token(self, token: str) -> TokenPayload:
        """
        Decodes the provided token and returns it
        """
        try:
            token_payload = jwt.decode(
                token, settings.JWT_SECRET_KEY, settings.ALGORITHM
            )

            return TokenPayload(**token_payload)
        except ExpiredSignatureError:
            raise Exception()


token_service = TokenService()
