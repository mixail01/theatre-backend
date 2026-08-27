from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.db import get_db
from src import entities, schemas


router = APIRouter(
    prefix="/actors",
    tags=["Actors"]
)


@router.post("/", response_model=schemas.ActorResponse, status_code=status.HTTP_201_CREATED)
async def create_actor(
    actor_data: schemas.ActorCreate,
    db: AsyncSession = Depends(get_db)
):
    new_actor = entities.Actor(**actor_data.model_dump())
    db.add(new_actor)
    await db.commit()
    await db.refresh(new_actor)
    return new_actor



@router.get("/", response_model=List[schemas.ActorResponse])
async def get_actors(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    query = select(entities.Actor).offset(skip).limit(limit)
    result = await db.execute(query)
    actors = result.scalars().all()
    return actors



@router.get("/{actor_id}", response_model=schemas.ActorResponse)
async def get_actor(
    actor_id: int,
    db: AsyncSession = Depends(get_db)
):
    actor = await db.get(entities.Actor, actor_id)
    if not actor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Актер с id={actor_id} не найден"
        )
    return actor



@router.put("/{actor_id}", response_model=schemas.ActorResponse)
async def update_actor(
    actor_id: int,
    actor_data: schemas.ActorCreate,
    db: AsyncSession = Depends(get_db)
):
    actor = await db.get(entities.Actor, actor_id)
    if not actor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Актер с id={actor_id} не найден"
        )

    actor.first_name = actor_data.first_name
    actor.last_name = actor_data.last_name

    await db.commit()
    await db.refresh(actor)
    return actor


# 5. Удаление актера
@router.delete("/{actor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_actor(
    actor_id: int,
    db: AsyncSession = Depends(get_db)
):
    actor = await db.get(entities.Actor, actor_id)
    if not actor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Актер с id={actor_id} не найден"
        )

    await db.delete(actor)
    await db.commit()
    return None
