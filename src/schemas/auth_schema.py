"""Auth schemas."""
from pydantic import BaseModel, EmailStr

from src.schemas.token_schema import Token


class AuthSchema(BaseModel):
    """Base model for the Authentication."""

    email: EmailStr
    password: str


class RefreshSchema(BaseModel):
    """Model for refreshing an outdated access token."""

    refresh_token: str


class AuthTokenSchema(BaseModel):
    """Model representing the access tokens."""

    access_token: Token
    refresh_token: Token
