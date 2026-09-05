from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.db import engine, Base
from src.routers import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):

    yield


app = FastAPI(title="Theatre API", lifespan=lifespan)
app.include_router(api_router)