# type: ignore
from typing import List
from sqlalchemy.ext.asyncio import AsyncResult

from sqlalchemy import update
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from models.user_model import User


class UserService():

    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def create_new_user(self, mail: str, password: str):
        self.db_session.add(User(email=mail, hash_password=password))
        result = await self.db_session.flush()

    async def get_user(self, mail: str) -> List[User]:
        res: AsyncResult = await self.db_session.execute(select(User).filter(User.email == mail))
        return res.all()
