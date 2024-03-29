from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext

from settings import settings

pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={"basic": "General scope for user", "admin": "Admin-only scope"},
)
GetTokenDep = Annotated[str, Depends(oauth2_scheme)]


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Getting a hash string from a password
    string depending on the declared CryptContext
    """
    return pwd_context.hash(password)


def create_access_token(data: dict):
    """
    Create Access token for `settings.access_token_expire_minutes` minutes
    """

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes,
    )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        claims=to_encode,
        key=settings.secret_key,
        algorithm=settings.secret_algorithm,
    )

    return encoded_jwt
