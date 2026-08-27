from datetime import datetime
from typing import List

from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db import Base


class Performance(Base):
    __tablename__ = "performances"

    id: Mapped[int] = mapped_column(primary_key=True)
    show_time: Mapped[datetime] = mapped_column(DateTime)

    play_id: Mapped[int] = mapped_column(ForeignKey("plays.id", ondelete="CASCADE"))
    theatre_hall_id: Mapped[int] = mapped_column(ForeignKey("theatre_halls.id", ondelete="CASCADE"))

    play: Mapped["Play"] = relationship(back_populates="performances")
    theatre_hall: Mapped["TheatreHall"] = relationship(back_populates="performances")

    tickets: Mapped[List["Ticket"]] = relationship(back_populates="performance")
