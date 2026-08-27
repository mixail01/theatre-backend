from datetime import datetime
from pydantic import BaseModel

from src.schemas.base import BaseResponseModel

from .hall import TheatreHallResponse
from .play import PlayResponse


class PerformanceBase(BaseModel):
    show_time: datetime


class PerformanceCreate(PerformanceBase):
    play_id: int
    theatre_hall_id: int


class PerformanceResponse(PerformanceBase, BaseResponseModel):
    play: PlayResponse
    theatre_hall: TheatreHallResponse
