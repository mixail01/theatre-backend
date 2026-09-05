from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.db import get_db
from src import entities, models
from src.core.security import get_current_user

from .models import ReservationPaymentModel


router = APIRouter(prefix="/reservations", tags=["Reservations"])


@router.post("/", response_model=models.ReservationResponse, status_code=status.HTTP_201_CREATED)
async def create_reservation(
    data: models.ReservationCreate,
    db: AsyncSession = Depends(get_db),
    user: entities.User = Depends(get_current_user),
):
    tickets = []
    for ticket_data in data.tickets:
        performance = await db.get(entities.Performance, ticket_data.performance_id)
        if not performance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Показ id={ticket_data.performance_id} не знайдено",
            )

        existing = await db.scalar(
            select(entities.Ticket).where(
                entities.Ticket.performance_id == ticket_data.performance_id,
                entities.Ticket.row == ticket_data.row,
                entities.Ticket.seat == ticket_data.seat,
                entities.Ticket.reservation_id.is_not(None),
            )
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Місце {ticket_data.row}/{ticket_data.seat} вже зайняте",
            )

        tickets.append(
            entities.Ticket(
                performance_id=ticket_data.performance_id,
                row=ticket_data.row,
                seat=ticket_data.seat,
            )
        )

    reservation = entities.Reservation(user_id=user.id, tickets=tickets)
    db.add(reservation)
    await db.commit()
    await db.refresh(reservation)
    return reservation


@router.get("/my", response_model=List[models.ReservationResponse])
async def get_my_reservations(
    db: AsyncSession = Depends(get_db),
    user: entities.User = Depends(get_current_user),
):
    result = await db.execute(
        select(entities.Reservation).where(entities.Reservation.user_id == user.id)
    )
    return result.scalars().all()


@router.delete("/{reservation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def cancel_reservation(
    reservation_id: int,
    db: AsyncSession = Depends(get_db),
    user: entities.User = Depends(get_current_user),
):
    reservation = await db.get(entities.Reservation, reservation_id)
    if not reservation or reservation.user_id != user.id:
        raise HTTPException(status_code=404, detail="Бронювання не знайдено")

    await db.delete(reservation)
    await db.commit()


@router.post("/payment", status_code=status.HTTP_202_ACCEPTED)
async def create_payment(
    payload: ReservationPaymentModel,
    db: AsyncSession = Depends(get_db),
    user: entities.User = Depends(get_current_user),
):
    return {"status": "accepted", "message": "Платіж прийнято до обробки"}