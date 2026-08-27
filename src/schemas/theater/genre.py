from pydantic import BaseModel

from src.schemas.base import BaseResponseModel


class GenreBase(BaseModel):
    name: str


class GenreCreate(GenreBase):
    pass


class GenreResponse(GenreBase, BaseResponseModel):
    pass
