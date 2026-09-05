from pydantic import BaseModel

from src.models.base import BaseResponseModel


class GenreBase(BaseModel):
    name: str


class GenreCreate(GenreBase):
    pass


class GenreResponse(GenreBase, BaseResponseModel):
    pass
