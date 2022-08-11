from datetime import datetime
from typing import Dict
from enum import Enum
from pydantic import BaseModel


class Token_Types(str, Enum):
    ACCESS_TOKEN = 'access_token'
    REFRESH_TOKEN = 'refresh_token'


class Token (BaseModel):
    token: str
    expires: datetime


class Auth_Token (BaseModel):
    __root__: Dict[str, Token]

    class Config:
        use_enum_values = True


class Token_Payload (BaseModel):
    sub: str
    iat: int
    exp: int
    type: Token_Types
