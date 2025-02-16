from fastapi import APIRouter, status

from backend.database import SessionDep
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
