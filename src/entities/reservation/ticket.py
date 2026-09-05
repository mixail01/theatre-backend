from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db import Base


class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(primary_key=True)
    row: Mapped[int]
    seat: Mapped[int]

    performance_id: Mapped[int] = mapped_column(ForeignKey("performances.id", ondelete="CASCADE"))
    reservation_id: Mapped[Optional[int]] = mapped_column(ForeignKey("reservations.id", ondelete="SET NULL"), nullable=True)

    performance: Mapped["Performance"] = relationship(back_populates="tickets")
    reservation: Mapped[Optional["Reservation"]] = relationship(back_populates="tickets")
