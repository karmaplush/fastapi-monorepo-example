import datetime
import uuid
from typing import Literal

from sqlalchemy import TIMESTAMP, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

Role = Literal["basic", "admin"]


class Model(DeclarativeBase):
    __abstract__ = True

    type_annotation_map = {
        datetime.datetime: TIMESTAMP(timezone=True),
    }

    id: Mapped[int] = mapped_column(primary_key=True)

    date_created: Mapped[datetime.datetime] = mapped_column(default=func.now())
    date_updated: Mapped[datetime.datetime] = mapped_column(
        default=func.now(),
        onupdate=func.now(),
    )


class UserModel(Model):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(
        String(320), index=True, unique=True, nullable=False
    )
    hashed_password: Mapped[str]

    role: Mapped[Role] = mapped_column(default="basic", nullable=False)

    threads: Mapped[list["ThreadModel"]] = relationship(back_populates="user")


class ThreadModel(Model):
    __tablename__ = "threads"

    article: Mapped[str] = mapped_column(index=True)
    guid: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["UserModel"] = relationship(back_populates="threads")
