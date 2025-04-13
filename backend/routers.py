from fastapi import APIRouter, FastAPI

from backend.common.route.constants.api_prefix import API_PREFIX
from backend.features.auth.routes import auth_router
from backend.features.hangman.routes import hangman_router
from backend.features.user.routes import user_router


def register_routers(app: FastAPI):
    api_router = APIRouter(prefix=API_PREFIX)

    api_router.include_router(user_router)
    api_router.include_router(auth_router)
    api_router.include_router(hangman_router)

    app.include_router(api_router)
