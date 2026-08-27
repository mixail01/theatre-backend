from typing import List

from sqlalchemy import String, Text, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db import Base


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
