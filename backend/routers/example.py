from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/")
def read_root():
    return JSONResponse(content={"message": "Welcome to FastAPI with Conda!"})
