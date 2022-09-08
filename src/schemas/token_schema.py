"""Token schemas."""
from datetime import datetime
from enum import Enum
from typing import Dict

from pydantic import BaseModel


class TokenTypes(str, Enum):
    """The types of tokens that can be issued."""

    ACCESS_TOKEN = "access_token"
    REFRESH_TOKEN = "refresh_token"


class Token(BaseModel):
    """The general ```Token``` object."""

    token: str
    expires: datetime


class AuthToken(BaseModel):
    """The auth token object that consist of a ```TokenTypes```and the ```Token``` itself."""

    __root__: Dict[TokenTypes, Token]

    class Config:
        """Configure the model to use enum values."""

        use_enum_values = True


class TokenPayload(BaseModel):
    """The decoded token payload."""

    sub: str
    iat: int
    exp: int
    type: TokenTypes
