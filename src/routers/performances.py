from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.db import get_db
from src import entities, models


router = APIRouter(prefix="/performances", tags=["Performances"])


@router.post("/", response_model=models.PerformanceResponse, status_code=status.HTTP_201_CREATED)
async def create_performance(
    performance_data: models.PerformanceCreate,
    db: AsyncSession = Depends(get_db)
):
    play = await db.get(entities.Play, performance_data.play_id)
    if not play:
        raise HTTPException(status_code=404, detail="Спектакль не знайдено")

    hall = await db.get(entities.TheatreHall, performance_data.theatre_hall_id)
    if not hall:
        raise HTTPException(status_code=404, detail="Зал не знайдено")

    new_performance = entities.Performance(**performance_data.model_dump())
    db.add(new_performance)
    await db.commit()
    await db.refresh(new_performance)
    return new_performance


@router.get("/", response_model=List[models.PerformanceResponse])
async def get_performances(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    query = select(entities.Performance).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{performance_id}", response_model=models.PerformanceResponse)
async def get_performance(
    performance_id: int,
    db: AsyncSession = Depends(get_db)
):
    performance = await db.get(entities.Performance, performance_id)
    if not performance:
        raise HTTPException(status_code=404, detail="Показ не знайдено")
    return performance


@router.delete("/{performance_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_performance(
    performance_id: int,
    db: AsyncSession = Depends(get_db)
):
    performance = await db.get(entities.Performance, performance_id)
    if not performance:
        raise HTTPException(status_code=404, detail="Показ не знайдено")

    await db.delete(performance)
    await db.commit()
    return None