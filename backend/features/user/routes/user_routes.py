from fastapi import APIRouter, Body, Depends, status

from backend.common.route.enums.api_routes import ApiRoutes
from backend.common.route.enums.api_tags import ApiTags
from backend.features.user.domain.models import UserCreate
from backend.features.user.domain.services.user_service import UserService
from backend.features.user.repositories.sql.entities import UserSqlEntity
from backend.features.user.routes.requests import UserCreateRequest

router = APIRouter(prefix=f"/{ApiRoutes.USER.value}", tags=[ApiTags.USER])


@router.post(
    "/",
    responses={
        status.HTTP_201_CREATED: {
            "description": "User successfully created",
            "model": UserSqlEntity,
        }
    },
    status_code=status.HTTP_201_CREATED,
    response_model=UserSqlEntity,
    summary="Create new user",
)
async def create_user(
    user_create_request: UserCreateRequest = Body(...),
    user_service: UserService = Depends(UserService),
) -> UserSqlEntity:
    user_create_model: UserCreate = user_create_request.to_create_model()
    return user_service.create_user(user_create_model)
