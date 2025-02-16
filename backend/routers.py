from fastapi import APIRouter, FastAPI

from backend.features.auth.routes import auth_router
from backend.features.user.routes import user_router
from backend.routes import items_router


def register_routers(app: FastAPI):
    api_router = APIRouter(prefix="/api")

    api_router.include_router(items_router)
    api_router.include_router(user_router)
    api_router.include_router(auth_router)

    app.include_router(api_router)
