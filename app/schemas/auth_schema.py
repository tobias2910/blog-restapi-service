from pydantic import BaseModel, EmailStr


class Auth_schema(BaseModel):
    """
    Base model for the Authentication
    """

    email: EmailStr
    password: str
