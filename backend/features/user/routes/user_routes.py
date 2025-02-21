from fastapi import APIRouter, status

from backend.common.route.enums.api_routes import ApiRoutes
from backend.common.route.enums.api_tags import ApiTags
from backend.database import SessionDep
from backend.features.user.repositories.entity.user_entity import User

router = APIRouter(prefix=f"/{ApiRoutes.USER.value}", tags=[ApiTags.USER])


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
