from data.models import UserModel
from repositories.base import BaseRepository


class UsersRepository(BaseRepository):
    model = UserModel
