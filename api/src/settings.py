from pydantic_settings import BaseSettings
from pydantic import PostgresDsn


class Settings(BaseSettings):
    debug: bool | None = False
    postgres_dsn: PostgresDsn = (
        "postgresql+asyncpg://postgres:postgrespwd@db:5432/database"
    )


settings = Settings()
