from pydantic import BaseModel


class DTOTokenOut(BaseModel):
    access_token: str
    token_type: str


class DTOTokenDataIn(BaseModel):
    username: str | None = None
    scopes: list[str] = []
