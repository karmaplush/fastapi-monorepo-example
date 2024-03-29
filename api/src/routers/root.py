from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from dto.token import DTOTokenOut
from services.users import UsersServiceDep

router = APIRouter(prefix="", tags=["root"])


@router.post("/token", response_model=DTOTokenOut)
async def login_for_token(
    users_service: UsersServiceDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    return await users_service.auth_and_login_user(
        username=form_data.username,
        password=form_data.password,
        scopes=form_data.scopes,
    )
