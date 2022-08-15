from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession  # type: ignore
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


from app.config.settings import settings

engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URI  # type: ignore
)

async_session = sessionmaker(
    engine,
    autocommit=False,
    autoflush=False,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncSession:
    '''
    Provides the session object, allowing to execute
    CRUD operations on the database.
    '''
    async with async_session() as session:
        session: AsyncSession
        yield session


Base = declarative_base()
