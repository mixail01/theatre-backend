from fastapi import APIRouter

from .reservations import router as reservation_router
from .actors import router as actors_router
from .auth import router as auth_router
from .genres import router as genres_router
from .halls import router as halls_router
from .performances import router as performances_router
from .plays import router as plays_router


api_router = APIRouter(prefix="/api")

api_router.include_router(auth_router)
api_router.include_router(actors_router)
api_router.include_router(genres_router)
api_router.include_router(halls_router)
api_router.include_router(plays_router)
api_router.include_router(performances_router)
api_router.include_router(reservation_router)


__all__ = [
    "api_router"
]
