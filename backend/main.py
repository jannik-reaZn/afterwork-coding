from fastapi import FastAPI

from backend.middlewares import register_middlewares
from backend.routers import register_routers

app = FastAPI()


register_middlewares(app)
register_routers(app)
