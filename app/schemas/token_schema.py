from enum import Enum
from pydantic import BaseModel


class Token_Types(Enum):
    ACCESS_TOKEN = 'access_token'
    REFRESH_TOKEN = 'refresh_token'


class Token (BaseModel):
    access_token: Token_Types
    token_type: str
