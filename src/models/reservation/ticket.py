from typing import Optional
from pydantic import BaseModel

from src.models.base import BaseResponseModel


class TicketBase(BaseModel):
    row: int
    seat: int


class TicketCreate(TicketBase):
    performance_id: int


class TicketResponse(TicketBase, BaseResponseModel):
    performance_id: int
    reservation_id: Optional[int] = None
