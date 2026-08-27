from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.db import engine, Base
from src.api import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # TODO: Убрать и добавить alembic
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="Theatre API", lifespan=lifespan)
app.include_router(api_router)
