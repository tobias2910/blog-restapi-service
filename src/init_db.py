"""Initializes the admin user in the DB if not already done."""
import asyncio
from typing import Union, cast

from sqlalchemy.ext.asyncio import AsyncSession

from src.config.settings import settings
from src.db.base import async_session
from src.schemas.user_schema import UserDB
from src.services.user_service import user_service


async def main() -> None:
    """Create admin user in the database.

    Checks, whether the admin user is already available in the
    database and if not, creates a new it.
    """
    async with async_session() as session:
        session = cast(AsyncSession, session)
        async with session.begin:
            res: Union[UserDB, None] = await user_service.get_user(session, settings.ADMIN_USER)
            if res is None:
                await user_service.create_new_user(session, settings.ADMIN_USER, settings.ADMIN_PW)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
