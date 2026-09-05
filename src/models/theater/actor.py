from pydantic import BaseModel

from src.models.base import BaseResponseModel


class ActorBase(BaseModel):
    first_name: str
    last_name: str


class ActorCreate(ActorBase):
    pass


class ActorResponse(ActorBase, BaseResponseModel):
    pass
