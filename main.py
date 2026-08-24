from contextlib import asynccontextmanager
from fastapi import FastAPI

from database import engine, Base
import models

from routers import (
    actors,
    genres,
    halls,
    plays,
    performances,
    reservations,
    auth,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="Theatre API", lifespan=lifespan)

app.include_router(auth.router)
app.include_router(actors.router)
app.include_router(genres.router)
app.include_router(halls.router)
app.include_router(plays.router)
app.include_router(performances.router)
app.include_router(reservations.router)