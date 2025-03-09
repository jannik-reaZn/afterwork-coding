from fastapi import FastAPI

from backend.handlers import register_exception_handlers
from backend.middlewares import register_middlewares
from backend.routers import register_routers

app = FastAPI()


register_middlewares(app)
register_exception_handlers(app)
register_routers(app)
