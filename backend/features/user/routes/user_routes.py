from http import HTTPStatus

from fastapi import APIRouter, Body, Depends, status

from backend.common.route.enums.api_routes import ApiRoutes
from backend.common.route.enums.api_tags import ApiTags
from backend.common.route.responses import Created, UnprocessableEntity
from backend.features.user.domain.example import USER_EXAMPLE
from backend.features.user.domain.models import User, UserCreate
from backend.features.user.domain.services.user_service import UserService
from backend.features.user.routes.requests import UserCreateRequest

router = APIRouter(prefix=f"/{ApiRoutes.USER.value}", tags=[ApiTags.USER])


@router.post(
    "/",
    responses={
        HTTPStatus.CREATED: Created.to_example(model=User, example=USER_EXAMPLE),
        HTTPStatus.UNPROCESSABLE_ENTITY: UnprocessableEntity.to_example(),
    },
    summary="Create new user",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    user_create_request: UserCreateRequest = Body(...),
    user_service: UserService = Depends(UserService),
) -> User:
    user_create_model: UserCreate = user_create_request.to_create_model()
    return user_service.create_user(user_create_model)


@router.get(
    "/{user_id}",
    summary="Get user by id",
    response_model=User,
    status_code=status.HTTP_200_OK,
)
async def get_user(
    user_id: int,
    user_service: UserService = Depends(UserService),
) -> User:
    return user_service.get_user(user_id)
