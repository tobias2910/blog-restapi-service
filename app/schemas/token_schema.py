from enum import Enum
from pydantic import BaseModel


class Token_Types(str, Enum):
    ACCESS_TOKEN = 'access_token'
    REFRESH_TOKEN = 'refresh_token'


class Token (BaseModel):
    token: str
    expires: str


class Auth_Token (BaseModel):
    Token_Types.ACCESS_TOKEN: Token
    Token_Types.REFRESH_TOKEN: Token
