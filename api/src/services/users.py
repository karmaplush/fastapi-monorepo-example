from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import SecurityScopes
from jose import JWTError, jwt
from pydantic import ValidationError

from data.models import UserModel
from data.uow import UOWDep
from dto.token import DTOTokenDataIn
from dto.users import DTORegistrationIn
from settings import settings
from utils.auth import (
    GetTokenDep,
    create_access_token,
    get_password_hash,
    verify_password,
)


class IncorrectUsernameOrPasswordHTTPException(HTTPException):

    def __init__(self) -> None:
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.detail = "Incorrect username or password"
        self.headers = {"WWW-Authenticate": "Bearer"}


class InvalidCredentialsHTTPException(HTTPException):

    def __init__(
        self,
        detail: str,
        headers: dict[str, str],
        status_code: int = status.HTTP_401_UNAUTHORIZED,
    ) -> None:
        self.status_code = status_code
        self.detail = detail
        if headers is None:
            self.headers = {"WWW-Authenticate": "Bearer"}
        else:
            self.headers = headers


class UsersService:
    """
    Service layer for interaction with Users logic

    Designed for using via Dependency Injection in FastAPI routes

    If some logic must be done without calling DB
    (=> without creating `UOW` instance), declarate it as `@classmethod`
    and call it directly from this class
    """

    def __init__(self, uow: UOWDep):
        self.uow = uow

    @classmethod
    async def no_db_logic(cls) -> None:
        print("Logic without creating UOW instance was called")
        return

    async def get_all_users(self) -> list[UserModel]:
        async with self.uow:
            return await self.uow.users.get_all()

    async def get_user_by_id(self, user_id: int) -> UserModel | None:
        async with self.uow:
            return await self.uow.users.get_one(id=user_id)

    async def get_user_by_email(self, user_email: str) -> UserModel | None:
        async with self.uow:
            return await self.uow.users.get_one(email=user_email)

    async def register_user(self, registration_data: DTORegistrationIn) -> None:

        registration_data: dict = registration_data.model_dump()
        plain_password = registration_data.pop("password")
        registration_data["hashed_password"] = get_password_hash(plain_password)

        async with self.uow:
            await self.uow.users.add(registration_data)
            await self.uow.commit()

    async def auth_and_login_user(
        self,
        username: str,
        password: str,
        scopes: list[str],
    ) -> dict:
        user = await self.get_user_by_email(user_email=username)

        if not user:
            raise IncorrectUsernameOrPasswordHTTPException

        if not verify_password(
            plain_password=password,
            hashed_password=user.hashed_password,
        ):
            raise IncorrectUsernameOrPasswordHTTPException

        # If user is not admin - only `basic` scope is available
        if user.role != "admin":
            scopes = ["basic"]

        access_token = create_access_token(
            data={
                "sub": user.email,
                "scopes": scopes,
            }
        )
        return {"access_token": access_token, "token_type": "bearer"}


UsersServiceDep = Annotated[UsersService, Depends()]


async def get_user_from_token(
    token: GetTokenDep,
    user_service: UsersServiceDep,
    security_scopes: SecurityScopes,
) -> UserModel:

    # XXX: Every time, if some error occured before
    # actual DB hit for getting user - one useless UsersService instance =>
    # useless UnitOfWork created. Need to fix this behavior.

    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )

    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.secret_algorithm],
        )
        user_email: str = payload.get("sub")

        if not user_email:
            raise credentials_exception

        token_scopes = payload.get("scopes", [])
        token_data = DTOTokenDataIn(username=user_email, scopes=token_scopes)

    except (JWTError, ValidationError):
        raise credentials_exception

    user = await user_service.get_user_by_email(user_email=token_data.username)

    if not user:
        credentials_exception

    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )

    return user
