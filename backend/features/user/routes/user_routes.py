from typing import Annotated

from fastapi import APIRouter, Depends, status

from backend.database import SessionDep
from backend.features.auth.domain.services import Oauth2SchemeDep, get_current_user
from backend.features.user.repositories.entity.user_entity import User

router = APIRouter(prefix="/user", tags=["user"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=User,
    summary="Create an new user",
)
async def create_user(user: User, session: SessionDep):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


@router.get("/", response_model=User, summary="Get the current user")
async def get_user(token: Oauth2SchemeDep):
    return {"token": token}
