from datetime import datetime
from enum import Enum
from typing import Dict

from pydantic import BaseModel


class TokenTypes(str, Enum):
    ACCESS_TOKEN = "access_token"
    REFRESH_TOKEN = "refresh_token"


class Token(BaseModel):
    token: str
    expires: datetime


class AuthToken(BaseModel):
    __root__: Dict[TokenTypes, Token]

    class Config:
        use_enum_values = True


class TokenPayload(BaseModel):
    sub: str
    iat: int
    exp: int
    type: TokenTypes
