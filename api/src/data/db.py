from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.settings import settings


class Model(DeclarativeBase):
    pass


engine: AsyncEngine = create_async_engine(str(settings.postgres_dsn))

session_maker = async_sessionmaker(engine, expire_on_commit=False)
