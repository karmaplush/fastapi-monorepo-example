import abc
from typing import Any, Type, TypeVar

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from data.models import Model

M = TypeVar("M", bound=Model)


class IRepository(abc.ABC):
    @abc.abstractmethod
    async def get_all(self) -> Any:
        raise NotImplementedError

    @abc.abstractmethod
    async def add(self, data: dict) -> int:
        raise NotImplementedError


class BaseRepository(IRepository):
    model: Type[M]
    db_session: AsyncSession

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_all(self) -> list[M]:
        stmt = select(self.model)
        result = await self.db_session.execute(stmt)
        return result.scalars().all()

    async def get_one(self, **filters) -> M | None:
        stmt = select(self.model).filter_by(**filters)
        result = await self.db_session.execute(stmt)
        return result.scalar_one_or_none()

    async def add(self, data: dict) -> int:
        stmt = insert(self.model).values(**data).returning(self.model.id)
        result = await self.db_session.execute(stmt)
        return result.scalar_one()
