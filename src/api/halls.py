from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.db import get_db
from src import entities, schemas

router = APIRouter(
    prefix="/halls",
    tags=["Theatre Halls"]
)


@router.post("/", response_model=schemas.TheatreHallResponse, status_code=status.HTTP_201_CREATED)
async def create_hall(
    hall_data: schemas.TheatreHallCreate,
    db: AsyncSession = Depends(get_db)
):
    new_hall = entities.TheatreHall(**hall_data.model_dump())
    db.add(new_hall)
    await db.commit()
    await db.refresh(new_hall)
    return new_hall


@router.get("/", response_model=List[schemas.TheatreHallResponse])
async def get_halls(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    query = select(entities.TheatreHall).offset(skip).limit(limit)
    result = await db.execute(query)
    halls = result.scalars().all()
    return halls


@router.get("/{hall_id}", response_model=schemas.TheatreHallResponse)
async def get_hall(
    hall_id: int,
    db: AsyncSession = Depends(get_db)
):
    hall = await db.get(entities.TheatreHall, hall_id)
    if not hall:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Зал с id={hall_id} не найден"
        )
    return hall


@router.put("/{hall_id}", response_model=schemas.TheatreHallResponse)
async def update_hall(
    hall_id: int,
    hall_data: schemas.TheatreHallCreate,
    db: AsyncSession = Depends(get_db)
):
    hall = await db.get(entities.TheatreHall, hall_id)
    if not hall:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Зал с id={hall_id} не найден"
        )

    hall.name = hall_data.name
    hall.rows = hall_data.rows
    hall.seats_in_row = hall_data.seats_in_row

    await db.commit()
    await db.refresh(hall)
    return hall


@router.delete("/{hall_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_hall(
    hall_id: int,
    db: AsyncSession = Depends(get_db)
):
    hall = await db.get(entities.TheatreHall, hall_id)
    if not hall:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Зал с id={hall_id} не найден"
        )

    await db.delete(hall)
    await db.commit()
    return None