from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    debug: bool | None = False

    postgres_dsn: PostgresDsn = (
        "postgresql+asyncpg://postgres:postgrespwd@db:5432/database"
    )

    secret_key: str | None = "fakesecret"
    secret_algorithm: str | None = "HS256"
    access_token_expire_minutes: int | None = 30


settings = Settings()
