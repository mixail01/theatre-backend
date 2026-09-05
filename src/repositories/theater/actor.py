from src.entities import Actor
from src.repositories.base import BaseRepository
from src.models import ActorResponse


class ActorRepository(BaseRepository[Actor, ActorResponse]):
    entity = Actor
    model = ActorResponse