from datetime import datetime, timedelta
from jose import jwt

from app.config.settings import settings
from app.schemas.token_schema import Token_Types, Token, Auth_Token, Token_Payload


class Token_service():
    '''
    Provides services for generating the auth tokens used
    to get access to protected endpoints
    '''

    def __generate_token(self, user_id: str, expires_in: int,
                         type: Token_Types, secret: str = settings.JWT_SECRET_KEY) -> str:
        '''
        Generates a new JWT token
        '''
        payload = {
            'sub': user_id,
            'iat': int(datetime.now().timestamp()),
            'exp': expires_in,
            'type': type,
        }

        return jwt.encode(payload, secret, algorithm=settings.ALGORITHM)

    def generate_auth_tokens(self, user_id: str) -> Auth_Token:
        '''
        Generates the access and refresh tokens
        '''
        access_token_expire = datetime.now(
        ) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_token_expire = datetime.now(
        ) + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)

        access_token = self.__generate_token(user_id, int(access_token_expire.timestamp()),
                                             Token_Types.ACCESS_TOKEN)
        refresh_token = self.__generate_token(user_id, int(refresh_token_expire.timestamp()),
                                              Token_Types.REFRESH_TOKEN, settings.JWT_REFRESH_SECRET_KEY)

        return Auth_Token(__root__={
            Token_Types.ACCESS_TOKEN: Token(
                token=access_token,
                expires=access_token_expire
            ),
            Token_Types.REFRESH_TOKEN.value: Token(
                token=refresh_token,
                expires=refresh_token_expire
            )}
        )

    def decode_token(self, token: str) -> Token_Payload:
        '''
        Decodes the provided token and returns it 
        '''
        token_payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, settings.ALGORITHM)

        return Token_Payload(**token_payload)


token_service = Token_service()
