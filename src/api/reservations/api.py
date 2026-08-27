from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.db import get_db
from src import entities, schemas
from src.core.security import get_current_user

from .models import ReservationPaymentModel


router = APIRouter(prefix="/reservations", tags=["Reservations"])


@router.post("/", response_model=schemas.ReservationResponse, status_code=status.HTTP_201_CREATED)
async def create_reservation(
    data: schemas.ReservationCreate,
    db: AsyncSession = Depends(get_db),
    user: entities.User = Depends(get_current_user)
):
    new_ticket = entities.Ticket(
        performance_id=data.performance_id,
        row=data.row,
        seat=data.seat
    )

    new_reservation = entities.Reservation(
        user_id=user.id,
        tickets=[new_ticket]
    )

    db.add(new_reservation)
    await db.commit()
    await db.refresh(new_reservation)
    return new_reservation


@router.get("/my", response_model=List[schemas.ReservationResponse])
async def get_my_reservations(
    db: AsyncSession = Depends(get_db),
    user: entities.User = Depends(get_current_user)
):
    query = select(entities.Reservation).where(entities.Reservation.user_id == user.id)
    result = await db.execute(query)
    return result.scalars().all()


@router.delete("/{reservation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def cancel_reservation(
    reservation_id: int,
    db: AsyncSession = Depends(get_db),
    user: entities.User = Depends(get_current_user)
):
    reservation = await db.get(entities.Reservation, reservation_id)
    if not reservation or reservation.user_id != user.id:
        raise HTTPException(status_code=404, detail="Бронювання не знайдено")

    await db.delete(reservation)
    await db.commit()
    return None


@router.post("/payment", status_code=status.HTTP_202_ACCEPTED)
async def create_payment(
    payload: ReservationPaymentModel,
    db: AsyncSession = Depends(get_db),
    user: entities.User = Depends(get_current_user)
):
    pass
