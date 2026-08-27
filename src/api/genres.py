from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.db import get_db
from src import entities, schemas


router = APIRouter(
    prefix="/genres",
    tags=["Genres"]
)


@router.post("/", response_model=schemas.GenreResponse, status_code=status.HTTP_201_CREATED)
async def create_genre(
    genre_data: schemas.GenreCreate,
    db: AsyncSession = Depends(get_db)
):
    new_genre = entities.Genre(**genre_data.model_dump())
    db.add(new_genre)
    await db.commit()
    await db.refresh(new_genre)
    return new_genre


@router.get("/", response_model=List[schemas.GenreResponse])
async def get_genres(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    query = select(entities.Genre).offset(skip).limit(limit)
    result = await db.execute(query)
    genres = result.scalars().all()
    return genres


@router.get("/{genre_id}", response_model=schemas.GenreResponse)
async def get_genre(
    genre_id: int,
    db: AsyncSession = Depends(get_db)
):
    genre = await db.get(entities.Genre, genre_id)
    if not genre:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Жанр с id={genre_id} не найден"
        )
    return genre


@router.put("/{genre_id}", response_model=schemas.GenreResponse)
async def update_genre(
    genre_id: int,
    genre_data: schemas.GenreCreate,
    db: AsyncSession = Depends(get_db)
):
    genre = await db.get(entities.Genre, genre_id)
    if not genre:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Жанр с id={genre_id} не найден"
        )

    genre.name = genre_data.name

    await db.commit()
    await db.refresh(genre)
    return genre


@router.delete("/{genre_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_genre(
    genre_id: int,
    db: AsyncSession = Depends(get_db)
):
    genre = await db.get(entities.Genre, genre_id)
    if not genre:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Жанр с id={genre_id} не найден"
        )

    await db.delete(genre)
    await db.commit()
    return None