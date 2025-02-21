from fastapi import APIRouter, Depends

from backend.common.route.enums.api_routes import ApiRoutes
from backend.common.route.enums.api_tags import ApiTags
from backend.features.auth.domain.services import AuthService, Oauth2SchemeDep
from backend.features.user.routes.dependency import get_auth_service

router = APIRouter(prefix=f"/{ApiRoutes.AUTH.value}", tags=[ApiTags.AUTH])


@router.get("/users/me")
async def read_users_me(
    token: Oauth2SchemeDep,
    auth_service: AuthService = Depends(get_auth_service),
):
    return await auth_service.get_current_user(token)
