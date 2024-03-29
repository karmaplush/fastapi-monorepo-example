from typing import Annotated

from fastapi import APIRouter, HTTPException, Security, status

from data.models import UserModel
from dto.users import DTORegistrationIn, DTOUserOut
from services.users import UsersServiceDep, get_user_from_token

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "/registration",
    response_model=DTOUserOut,
    status_code=status.HTTP_201_CREATED,
)
async def registration(
    request: DTORegistrationIn,
    users_service: UsersServiceDep,
):
    return users_service.register_user(request)


@router.get("/me", response_model=DTOUserOut)
async def read_users_me(
    user: Annotated[UserModel, Security(get_user_from_token, scopes=["admin"])]
):
    return user


@router.get("/{user_id}", response_model=DTOUserOut | None)
async def read_user_by_id(users_service: UsersServiceDep, user_id: int):
    user = await users_service.get_user_by_id(user_id)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return user


@router.get("/", response_model=list[DTOUserOut])
async def read_all_users(users_service: UsersServiceDep):
    await users_service.__class__.no_db_logic()
    return await users_service.get_all_users()
