from datetime import datetime, timedelta
from jose import jwt

from config.settings import Settings
from schemas.token_schema import Token_Types


class Token_service():

    def __generate_token(self, user_id: str, expires_in: int,
                         type: Token_Types, secret: str = Settings.JWT_SECRET_KEY) -> str:
        '''
        Generates a new JWT token
        '''

        payload = {
            'sub': user_id,
            'iat': int(datetime.now().timestamp()),
            'exp': expires_in,
            'type': type,
        }

        return jwt.encode(payload, secret, algorithm=Settings.ALGORITHM)

    def generate_auth_tokens(self, user_id: str) -> dict[str, dict[str, str]]:
        '''
        Generates the access and refresh tokens
        '''
        access_token_expire = datetime.now(
        ) + timedelta(minutes=Settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_token_expire = datetime.now(
        ) + timedelta(minutes=Settings.REFRESH_TOKEN_EXPIRE_MINUTES)

        access_token = self.__generate_token(user_id, int(access_token_expire.timestamp()),
                                             Token_Types.ACCESS_TOKEN)
        refresh_token = self.__generate_token(user_id, int(refresh_token_expire.timestamp()),
                                              Token_Types.REFRESH_TOKEN, Settings.JWT_REFRESH_SECRET_KEY)

        return {
            'access': {
                'token': access_token,
                'expires': str(access_token_expire),
            },
            'refresh': {
                'token': refresh_token,
                'expires': str(refresh_token_expire)
            }
        }
