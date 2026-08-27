from typing import List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db import Base


class TheatreHall(Base):
    __tablename__ = "theatre_halls"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    rows: Mapped[int]
    seats_in_row: Mapped[int]

    performances: Mapped[List["Performance"]] = relationship(back_populates="theatre_hall")
