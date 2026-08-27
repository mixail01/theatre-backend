from src.entities import Actor
from src.repositories.base import BaseRepository
from src.schemas import ActorResponse


class ActorRepository(BaseRepository):
    entity = Actor
    model = ActorResponse
