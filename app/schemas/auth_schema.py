from pydantic import BaseModel, EmailStr


class AuthSchema(BaseModel):
    """
    Base model for the Authentication
    """

    email: EmailStr
    password: str
