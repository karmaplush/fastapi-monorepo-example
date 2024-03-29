from data.models import ThreadModel
from repositories.base import BaseRepository


class ThreadsRepository(BaseRepository):
    model = ThreadModel
