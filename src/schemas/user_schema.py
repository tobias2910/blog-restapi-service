from pydantic import BaseModel, Field


class UserSchema(BaseModel):
    """
    The base model for managing users
    """

    email: str = Field(example="tobiascaliskan@gmx.de")


class CreateUser(UserSchema):
    """
    The model for creating a new user
    """

    password: str = Field(example="mysupersecretpassword")


class UserCreated(UserSchema):
    """
    The model for created users
    """

    status: str = Field(example="User successfully created")


class UserDeleted(UserSchema):
    """
    The model for deleting a user
    """

    status: str = Field(example="User successfully deleted")


class UserDB(UserSchema):
    """
    The model representing the result from the DB
    """

    id: int
    password: str = Field(example="mysupersecretpassword")
