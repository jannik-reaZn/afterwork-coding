from fastapi import APIRouter, FastAPI

from backend.routes import example_router, items_router, user_router


def register_routers(app: FastAPI):
    api_router = APIRouter(prefix="/api")

    api_router.include_router(example_router)
    api_router.include_router(items_router)
    api_router.include_router(user_router)

    app.include_router(api_router)
