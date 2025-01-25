from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import example_router, items_router
from .database import create_db_and_tables

create_db_and_tables()
app = FastAPI()


# NOTE This is bad practice and should be revisited!
# origins = ["http://localhost:5173/"]
origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(example_router)
app.include_router(items_router)
