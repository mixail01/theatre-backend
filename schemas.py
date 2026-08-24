from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, EmailStr


class ActorBase(BaseModel):
    first_name: str
    last_name: str


class ActorCreate(ActorBase):
    pass


class ActorResponse(ActorBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class GenreBase(BaseModel):
    name: str


class GenreCreate(GenreBase):
    pass


class GenreResponse(GenreBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class TheatreHallBase(BaseModel):
    name: str
    rows: int
    seats_in_row: int


class TheatreHallCreate(TheatreHallBase):
    pass


class TheatreHallResponse(TheatreHallBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class PlayBase(BaseModel):
    title: str
    description: str


class PlayCreate(PlayBase):
    genre_ids: List[int] = []
    actor_ids: List[int] = []


class PlayResponse(PlayBase):
    id: int
    genres: List[GenreResponse] = []
    actors: List[ActorResponse] = []

    model_config = ConfigDict(from_attributes=True)


class PerformanceBase(BaseModel):
    show_time: datetime


class PerformanceCreate(PerformanceBase):
    play_id: int
    theatre_hall_id: int


class PerformanceResponse(PerformanceBase):
    id: int
    play: PlayResponse
    theatre_hall: TheatreHallResponse

    model_config = ConfigDict(from_attributes=True)


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class TicketBase(BaseModel):
    row: int
    seat: int


class TicketCreate(TicketBase):
    performance_id: int


class TicketResponse(TicketBase):
    id: int
    performance_id: int
    reservation_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class ReservationCreate(BaseModel):
    tickets: List[TicketCreate]


class ReservationResponse(BaseModel):
    id: int
    created_at: datetime
    user_id: int
    tickets: List[TicketResponse] = []

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None