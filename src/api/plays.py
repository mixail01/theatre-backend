from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.db import get_db
from src import entities, schemas


router = APIRouter(
    prefix="/plays",
    tags=["Plays"]
)


@router.post("/", response_model=schemas.PlayResponse, status_code=status.HTTP_201_CREATED)
async def create_play(
    play_data: schemas.PlayCreate,
    db: AsyncSession = Depends(get_db)
):
    new_play = entities.Play(
        title=play_data.title,
        description=play_data.description
    )

    if play_data.genre_ids:
        genres_query = select(entities.Genre).where(entities.Genre.id.in_(play_data.genre_ids))
        genres_result = await db.execute(genres_query)
        new_play.genres = list(genres_result.scalars().all())

    if play_data.actor_ids:
        actors_query = select(entities.Actor).where(entities.Actor.id.in_(play_data.actor_ids))
        actors_result = await db.execute(actors_query)
        new_play.actors = list(actors_result.scalars().all())

    db.add(new_play)
    await db.commit()

    query = (
        select(entities.Play)
        .options(selectinload(entities.Play.genres), selectinload(entities.Play.actors))
        .where(entities.Play.id == new_play.id)
    )
    result = await db.execute(query)
    return result.scalar_one()


@router.get("/", response_model=List[schemas.PlayResponse])
async def get_plays(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    query = (
        select(entities.Play)
        .options(selectinload(entities.Play.genres), selectinload(entities.Play.actors))
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{play_id}", response_model=schemas.PlayResponse)
async def get_play(
    play_id: int,
    db: AsyncSession = Depends(get_db)
):
    query = (
        select(entities.Play)
        .options(selectinload(entities.Play.genres), selectinload(entities.Play.actors))
        .where(entities.Play.id == play_id)
    )
    result = await db.execute(query)
    play = result.scalar_one_or_none()

    if not play:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Спектакль с id={play_id} не найден"
        )
    return play


@router.put("/{play_id}", response_model=schemas.PlayResponse)
async def update_play(
    play_id: int,
    play_data: schemas.PlayCreate,
    db: AsyncSession = Depends(get_db)
):
    query = (
        select(entities.Play)
        .options(selectinload(entities.Play.genres), selectinload(entities.Play.actors))
        .where(entities.Play.id == play_id)
    )
    result = await db.execute(query)
    play = result.scalar_one_or_none()

    if not play:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Спектакль с id={play_id} не найден"
        )

    play.title = play_data.title
    play.description = play_data.description

    if play_data.genre_ids is not None:
        genres_query = select(entities.Genre).where(entities.Genre.id.in_(play_data.genre_ids))
        genres_result = await db.execute(genres_query)
        play.genres = list(genres_result.scalars().all())

    if play_data.actor_ids is not None:
        actors_query = select(entities.Actor).where(entities.Actor.id.in_(play_data.actor_ids))
        actors_result = await db.execute(actors_query)
        play.actors = list(actors_result.scalars().all())

    await db.commit()
    return play


@router.delete("/{play_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_play(
    play_id: int,
    db: AsyncSession = Depends(get_db)
):
    play = await db.get(entities.Play, play_id)
    if not play:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Спектакль с id={play_id} не найден"
        )

    await db.delete(play)
    await db.commit()
    return None