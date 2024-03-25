import datetime

from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import expression
from sqlalchemy.types import DateTime

from src.data.db import Model


class utcnow(expression.FunctionElement):
    type = DateTime()
    inherit_cache = True


@compiles(utcnow, "postgresql")
def pg_utcnow(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"


class UserModel(Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)

    username: Mapped[str] = mapped_column(index=True, unique=True)
    email: Mapped[str] = mapped_column(index=True, unique=True)
    hashed_password: Mapped[str]

    is_superuser: Mapped[bool] = mapped_column(default=False)

    timestamp_created: Mapped[datetime.datetime] = mapped_column(
        server_default=utcnow()
    )
    timestamp_updated: Mapped[datetime.datetime] = mapped_column(
        server_onupdate=utcnow()
    )
