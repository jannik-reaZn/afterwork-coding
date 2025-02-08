from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from backend.auth import get_current_user
from backend.auth.auth_bearer import oauth2_scheme_dep
from backend.database import get_db
from backend.db import User

router = APIRouter(prefix="/user", tags=["user"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=User,
    summary="Create an new user",
)
async def create_user(user: User, session: Session = Depends(get_db)):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


@router.get("/", response_model=User, summary="Get the current user")
async def get_user(token: oauth2_scheme_dep):
    return {"token": token}
