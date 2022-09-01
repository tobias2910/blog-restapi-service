from typing import Union

from src.models.user_model import User
from src.schemas.user_schema import UserCreated, UserDeleted
from fastapi import HTTPException, status
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncResult
from sqlalchemy.future import select
from sqlalchemy.orm import Session


class UserService:
    """
    Provides all user related services
    """

    async def create_new_user(
        self, db_session: Session, mail: str, password: str
    ) -> UserCreated:
        """
        Creates a new user in the database
        """
        try:
            user_in_db = await self.get_user(db_session, mail)
            if user_in_db is None:
                new_user = User(email=mail, hash_password=password)
                db_session.add(new_user)

                await db_session.commit()

                return {"email": mail, "status": "User successfully created"}
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Mail already used. Please provide another one.",
            )
        except HTTPException as e:
            raise (e)
        except BaseException:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error creating the user in the DB",
            )

    async def get_user(self, db_session: Session, mail: str) -> Union[User, None]:
        """
        Returns the matched user based on the provided ID
        """
        try:
            res: AsyncResult = await db_session.execute(
                select(User).where(User.email == mail)
            )
            user: User = res.scalars().first()

            if user is not None:
                return user
        except BaseException:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error obtaining the specified user from the database",
            )

    async def delete_user(self, db_session: Session, mail: str) -> UserDeleted:
        """
        Deletes the specified user
        """
        try:
            res: AsyncResult = await db_session.execute(
                delete(User).where(User.email == mail)
            )
            if res.rowcount != 0:
                await db_session.commit()
                return {"email": mail, "status": "User deleted"}
            return {"email": mail, "status": "User not found"}
        except BaseException:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error deleting the specified user in the database",
            )


user_service = UserService()
