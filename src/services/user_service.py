"""User services."""
from typing import Union

from fastapi import HTTPException, status
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncResult
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from src.models.user_model import User
from src.schemas.user_schema import UserCreated, UserDeleted


class UserService:
    """Provides all user related services."""

    async def create_new_user(self, db_session: Session, mail: str, password: str) -> UserCreated:
        """Create a new user in the database.

        Args:
            db_session (Session): The session for the DB.
            mail (str): The mail address of the new user.
            password (str): The password of the new user.

        Raises:
            HTTPException: Raised, in case the mail is already taken.
            HTTPException: Raised, in case any other errors occur during the creation.

        Returns:
            UserCreated: The status, that the user has been successfully created.
        """
        try:
            user_in_db = await self.get_user(db_session, mail)
            if user_in_db is None:
                new_user = User(email=mail, hash_password=password)
                db_session.add(new_user)

                await db_session.commit()  # type: ignore[func-returns-value]

                return {"email": mail, "status": "User successfully created"}
            raise HTTPException(  # noqa: TC301
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Mail already used. Please provide another one.",
            )
        except HTTPException:
            raise
        except BaseException:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error creating the user in the DB",
            ) from BaseException

    async def get_user(self, db_session: Session, mail: str) -> Union[User, None]:
        """Get the user from the DB.

        Returns the matched user based on the provided ID.

        Args:
            db_session (Session): The session for the DB.
            mail (str): The mail of the user to obtain.

        Raises:
            HTTPException: Raised, in case there is an error when obtaining the user.

        Returns:
            Union[User, None]: Can be either the user information ```User``` in case it is
            available or ```None```.
        """
        try:
            res: AsyncResult = await db_session.execute(select(User).where(User.email == mail))
            user: User = res.scalars().first()

            if user is not None:
                return user
            else:
                return None
        except BaseException:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error obtaining the specified user from the database",
            ) from BaseException

    async def delete_user(self, db_session: Session, mail: str) -> UserDeleted:
        """Delete the specified user.

        Args:
            db_session (Session): The session for the db.
            mail (str): The mail address of the user to delete.

        Raises:
            HTTPException: Raised, in case there is an error when deleting the user.

        Returns:
            UserDeleted: The status indicating, whether the deletion was successful.
        """
        try:
            res: AsyncResult = await db_session.execute(delete(User).where(User.email == mail))
            if res.rowcount != 0:
                await db_session.commit()  # type: ignore[func-returns-value]
                return {"email": mail, "status": "User deleted"}
            else:
                return {"email": mail, "status": "User not found"}
        except BaseException:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error deleting the specified user in the database",
            ) from BaseException


user_service = UserService()
