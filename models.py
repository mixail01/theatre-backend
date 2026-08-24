from datetime import datetime
from typing import List, Optional

from sqlalchemy import String, Text, ForeignKey, Table, Column, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


play_actor_association = Table(
    "play_actor_association",
    Base.metadata,
    Column("play_id", ForeignKey("plays.id", ondelete="CASCADE"), primary_key=True),
    Column("actor_id", ForeignKey("actors.id", ondelete="CASCADE"), primary_key=True),
)

play_genre_association = Table(
    "play_genre_association",
    Base.metadata,
    Column("play_id", ForeignKey("plays.id", ondelete="CASCADE"), primary_key=True),
    Column("genre_id", ForeignKey("genres.id", ondelete="CASCADE"), primary_key=True),
)


class Actor(Base):
    __tablename__ = "actors"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))

    plays: Mapped[List["Play"]] = relationship(
        secondary=play_actor_association,
        back_populates="actors"
    )


class Genre(Base):
    __tablename__ = "genres"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))

    plays: Mapped[List["Play"]] = relationship(
        secondary=play_genre_association,
        back_populates="genres"
    )


class TheatreHall(Base):
    __tablename__ = "theatre_halls"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    rows: Mapped[int]
    seats_in_row: Mapped[int]

    performances: Mapped[List["Performance"]] = relationship(back_populates="theatre_hall")


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))

    reservations: Mapped[List["Reservation"]] = relationship(back_populates="user")


class Play(Base):
    __tablename__ = "plays"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(150))
    description: Mapped[str] = mapped_column(Text)

    genres: Mapped[List[Genre]] = relationship(
        secondary=play_genre_association,
        back_populates="plays"
    )
    actors: Mapped[List[Actor]] = relationship(
        secondary=play_actor_association,
        back_populates="plays"
    )

    performances: Mapped[List["Performance"]] = relationship(back_populates="play")


class Performance(Base):
    __tablename__ = "performances"

    id: Mapped[int] = mapped_column(primary_key=True)
    show_time: Mapped[datetime] = mapped_column(DateTime)

    play_id: Mapped[int] = mapped_column(ForeignKey("plays.id", ondelete="CASCADE"))
    theatre_hall_id: Mapped[int] = mapped_column(ForeignKey("theatre_halls.id", ondelete="CASCADE"))

    play: Mapped[Play] = relationship(back_populates="performances")
    theatre_hall: Mapped[TheatreHall] = relationship(back_populates="performances")

    tickets: Mapped[List["Ticket"]] = relationship(back_populates="performance")


class Reservation(Base):
    __tablename__ = "reservations"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    user: Mapped[User] = relationship(back_populates="reservations")
    tickets: Mapped[List["Ticket"]] = relationship(back_populates="reservation")


class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(primary_key=True)
    row: Mapped[int]
    seat: Mapped[int]

    performance_id: Mapped[int] = mapped_column(ForeignKey("performances.id", ondelete="CASCADE"))
    reservation_id: Mapped[Optional[int]] = mapped_column(ForeignKey("reservations.id", ondelete="SET NULL"), nullable=True)

    performance: Mapped[Performance] = relationship(back_populates="tickets")
    reservation: Mapped[Optional[Reservation]] = relationship(back_populates="tickets")