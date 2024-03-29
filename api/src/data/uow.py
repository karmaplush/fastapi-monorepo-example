from abc import ABC, abstractmethod
from typing import Annotated, Type

from fastapi import Depends

from data.db import async_session_maker
from repositories.threads import ThreadsRepository
from repositories.users import UsersRepository


class IUnitOfWork(ABC):

    users: Type[UsersRepository]
    threads: Type[ThreadsRepository]

    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    async def __aenter__(self):
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(
        self,
        exception_type,
        exception_value,
        exception_traceback,
    ):
        raise NotImplementedError

    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError


class SqlAlchemyUnitOfWork(IUnitOfWork):

    def __init__(self):
        self.session_maker = async_session_maker

    async def __aenter__(self):
        self.session = self.session_maker()

        self.users = UsersRepository(self.session)
        self.threads = ThreadsRepository(self.session)

    async def __aexit__(
        self,
        exception_type,
        exception_value,
        exception_traceback,
    ):
        if exception_type:
            await self.session.rollback()
            # TODO: Log

        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()


UOWDep = Annotated[IUnitOfWork, Depends(SqlAlchemyUnitOfWork)]
