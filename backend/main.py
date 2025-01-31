from fastapi import FastAPI
from backend.database import create_db_and_tables
from backend.middlewares import register_middlewares
from backend.routers import register_routers 

create_db_and_tables()
app = FastAPI()


register_middlewares(app)
register_routers(app)
