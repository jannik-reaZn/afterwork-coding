from fastapi import APIRouter, Depends, status

from backend.database import SessionDep
from backend.features.auth.domain.services import AuthService, Oauth2SchemeDep
from backend.features.user.repositories.entity.user_entity import User
from backend.features.user.routes.dependency import get_auth_service

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
async def read_users_me(
    token: Oauth2SchemeDep,
    auth_service: AuthService = Depends(get_auth_service),
):
    return await auth_service.get_current_user(token)


@router.get("/", response_model=User, summary="Get the current user")
async def get_user(token: Oauth2SchemeDep):
    return {"token": token}
