from datetime import datetime
from typing import List
from pydantic import BaseModel

from src.schemas.base import BaseResponseModel

from .ticket import TicketCreate, TicketResponse


class ReservationCreate(BaseModel):
    tickets: List[TicketCreate]


class ReservationResponse(BaseResponseModel):
    created_at: datetime
    user_id: int
    tickets: List[TicketResponse] = []
