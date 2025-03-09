from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.common.config import settings


def register_middlewares(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
