from datetime import timedelta
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import HTTPException, status
from passlib.context import CryptContext

from backend.common.config import SettingsDependency
from backend.features.auth.domain.services.auth_service import AuthService
from backend.features.auth.repositories.auth_repository import AuthRepository
from backend.features.user.domain.services.user_service import UserService
from backend.features.user.repositories.sql.entities import UserSqlEntity
from backend.features.user.repositories.user_repository import UserRepository

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@pytest.fixture
def settings():
    mock_settings = MagicMock(spec=SettingsDependency)
    mock_settings.secret_key_jwt = "test_secret"
    mock_settings.algorithm_jwt = "HS256"
    return mock_settings


@pytest.fixture
def auth_repo():
    return AsyncMock(spec=AuthRepository)


@pytest.fixture
def auth_service(settings, auth_repo, user_service):
    return AuthService(settings=settings, auth_repo=auth_repo, user_service=user_service)


@pytest.fixture
def user_repo():
    return AsyncMock(spec=UserRepository)


@pytest.fixture
def user_service(user_repo):
    return AsyncMock(spec=UserService, user_repo=user_repo)


@pytest.mark.asyncio
async def test_authenticate_user_success(auth_service, user_service):
    # GIVEN
    user = UserSqlEntity(username="testuser", hashed_password=pwd_context.hash("testpassword"))
    user_service.get_user_by_username = AsyncMock(return_value=user)

    # WHEN
    authenticated_user = await auth_service.authenticate_user("testuser", "testpassword")

    # THEN
    assert authenticated_user == user


@pytest.mark.asyncio
async def test_authenticate_user_failure(auth_service, user_service):
    # GIVEN
    user_service.get_user_by_username = AsyncMock(return_value=None)

    # WHEN
    authenticated_user = await auth_service.authenticate_user("testuser", "wrongpassword")

    # THEN
    assert authenticated_user is False


def test_create_access_token(auth_service):
    # GIVEN
    data = {"sub": "testuser"}

    # WHEN
    token = auth_service.create_access_token(data=data, expires_delta=timedelta(minutes=30))

    # THEN
    assert token is not None


@pytest.mark.asyncio
async def test_get_current_user_success(auth_service, user_service):
    # GIVEN
    user = UserSqlEntity(username="testuser", hashed_password="hashedpassword")
    user_service.get_user_by_username = AsyncMock(return_value=user)

    # WHEN
    token = auth_service.create_access_token(data={"sub": "testuser"})
    current_user = await auth_service.get_current_user(token)

    # THEN
    assert current_user == user


@pytest.mark.asyncio
async def test_get_current_user_failure(auth_service, user_service):
    # GIVEN
    user_service.get_user_by_username = AsyncMock(return_value=None)

    # WHEN
    token = auth_service.create_access_token(data={"sub": "testuser"})
    with pytest.raises(HTTPException) as exc_info:
        await auth_service.get_current_user(token)

    # THEN
    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_login_success(auth_service, user_service):
    # GIVEN
    user = UserSqlEntity(username="testuser", hashed_password=pwd_context.hash("testpassword"))
    user_service.get_user_by_username = AsyncMock(return_value=user)

    form_data = MagicMock()
    form_data.username = "testuser"
    form_data.password = "testpassword"

    # WHEN
    token = await auth_service.login_for_access_token(form_data)

    # THEN
    assert token.token_type == "bearer"
    assert token.access_token is not None


@pytest.mark.asyncio
async def test_login_failure(auth_service, user_service):
    # GIVEN
    user_service.get_user_by_username = AsyncMock(return_value=None)

    form_data = MagicMock()
    form_data.username = "testuser"
    form_data.password = "wrongpassword"

    # WHEN
    with pytest.raises(HTTPException) as exc_info:
        await auth_service.login_for_access_token(form_data)

    # THEN
    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
