from pydantic import BaseModel

from src.models.base import BaseResponseModel


class TheatreHallBase(BaseModel):
    name: str
    rows: int
    seats_in_row: int


class TheatreHallCreate(TheatreHallBase):
    pass


class TheatreHallResponse(TheatreHallBase, BaseResponseModel):
    pass
