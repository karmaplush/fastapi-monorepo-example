from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine

from settings import settings

engine: AsyncEngine = create_async_engine(
    url=str(settings.postgres_dsn),
    echo=settings.debug,
)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
