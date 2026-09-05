from typing import List
from pydantic import BaseModel, ConfigDict

from src.models.base import BaseResponseModel

from .actor import ActorResponse
from .genre import GenreResponse


class PlayBase(BaseModel):
    title: str
    description: str


class PlayCreate(PlayBase):
    genre_ids: List[int] = []
    actor_ids: List[int] = []


class PlayResponse(PlayBase, BaseResponseModel):
    genres: List[GenreResponse] = []
    actors: List[ActorResponse] = []

    model_config = ConfigDict(from_attributes=True)
