import asyncio
from db.base import async_session
from sqlalchemy.orm import Session
from services.user_service import User_service
from config.settings import settings


async def main():
    async with async_session() as session:
        session: Session
        async with session.begin:  # type: ignore
            user_service = User_service(session)
            res = await user_service.get_user(settings.ADMIN_USER)
            if (len(res) == 0):
                await user_service.create_new_user(settings.ADMIN_USER, settings.ADMIN_PW)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
