from fastapi import APIRouter, Depends, status

from backend.common.route.enums.api_routes import ApiRoutes
from backend.common.route.enums.api_tags import ApiTags
from backend.features.user.domain.services.user_service import UserService
from backend.features.user.repositories.sql.entities.user_entity import UserSqlEntity

router = APIRouter(prefix=f"/{ApiRoutes.USER.value}", tags=[ApiTags.USER])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=UserSqlEntity,
    summary="Create new user",
)
async def create_user(
    user: UserSqlEntity, user_service: UserService = Depends(UserService)
) -> UserSqlEntity:
    return user_service.create_user(user)
