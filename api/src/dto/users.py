import datetime

from pydantic import BaseModel, EmailStr

from data.models import Role


class DTORegistrationIn(BaseModel):
    email: EmailStr
    password: str


class DTOUserOut(BaseModel):

    id: int
    email: EmailStr
    role: Role
    date_created: datetime.datetime
    date_updated: datetime.datetime
