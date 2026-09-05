from typing import Generic, TypeVar, Type, Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from src.db import Base

EntityType = TypeVar("EntityType", bound=Base)
SchemaType = TypeVar("SchemaType", bound=BaseModel)


class BaseRepository(Generic[EntityType, SchemaType]):
    entity: Type[EntityType]
    model: Type[SchemaType]

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, id: int) -> EntityType | None:
        return await self.db.get(self.entity, id)

    async def list(self, skip: int = 0, limit: int = 100) -> Sequence[EntityType]:
        result = await self.db.execute(
            select(self.entity).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def create(self, data: dict) -> EntityType:
        instance = self.entity(**data)
        self.db.add(instance)
        await self.db.commit()
        await self.db.refresh(instance)
        return instance

    async def update(self, instance: EntityType, data: dict) -> EntityType:
        for key, value in data.items():
            setattr(instance, key, value)
        await self.db.commit()
        await self.db.refresh(instance)
        return instance

    async def delete(self, instance: EntityType) -> None:
        await self.db.delete(instance)
        await self.db.commit()