# type: ignore
from typing import Union

from sqlalchemy.ext.asyncio import AsyncResult

from sqlalchemy.future import select
from sqlalchemy.orm import Session

from app.models.user_model import User


class User_service:
    """
    Provides all user related services
    """

    async def create_new_user(self, db_session: Session, mail: str, password: str):
        """
        Creates a new user in the database
        """
        db_session.add(User(email=mail, hash_password=password))
        res = await db_session.flush()
        return res

    async def get_user(self, db_session: Session, mail: str) -> Union[User, None]:
        """
        Returns the matched user based on the provided ID
        """
        res: AsyncResult = await db_session.execute(
            select(User).where(User.email == mail)
        )
        return res.scalars().first()


user_service = User_service()
