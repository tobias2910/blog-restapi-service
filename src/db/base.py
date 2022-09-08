"""Base settings for interacting with the database."""
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.config.settings import settings

engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI)

async_session = sessionmaker(
    engine,
    autocommit=False,
    autoflush=False,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncSession:
    """Session generator.

    Provides a new session that allows, to conduct CRUD actions
    on the database.

    Yields:
        Iterator[AsyncSession]: The session instance to use for conducting operations
    """
    session: AsyncSession = None

    try:
        async with async_session() as session:
            yield session
    except BaseException:
        if session is not None:
            await session.rollback()
        raise
    finally:
        if session is not None:
            await session.close()


Base = declarative_base()
