from fastapi import APIRouter, Depends

from backend.common.route.enums.api_routes import ApiRoutes
from backend.common.route.enums.api_tags import ApiTags
from backend.features.auth.domain.models import Token
from backend.features.auth.domain.services import (
    AuthService,
    OAuth2PasswordRequestFormDependency,
    Oauth2SchemeDep,
)

router = APIRouter(prefix=f"/{ApiRoutes.AUTH.value}", tags=[ApiTags.AUTH])


@router.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestFormDependency,
    auth_service: AuthService = Depends(AuthService),
) -> Token:
    return await auth_service.login(form_data)


@router.get("/users/me")
async def read_users_me(
    token: Oauth2SchemeDep,
    auth_service: AuthService = Depends(AuthService),
):
    return await auth_service.get_current_user(token)
