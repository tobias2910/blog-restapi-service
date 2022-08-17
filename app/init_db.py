from typing import Union
import asyncio
from db.base import async_session
from sqlalchemy.orm import Session
from app.services.user_service import User_service
from app.config.settings import settings
from app.schemas.user_schema import User


async def main():
    async with async_session() as session:
        session: Session
        async with session.begin:
            user_service = User_service(session)
            res: Union[User, None] = await user_service.get_user(settings.ADMIN_USER)
            if res is None:
                await user_service.create_new_user(
                    settings.ADMIN_USER, settings.ADMIN_PW
                )


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
