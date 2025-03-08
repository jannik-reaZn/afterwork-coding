from unittest.mock import AsyncMock, MagicMock

import pytest

from backend.common.config import SettingsDependency
from backend.features.auth.domain.services.auth_service import AuthService
from backend.features.auth.repositories.auth_repository import AuthRepository


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
def auth_service(settings, auth_repo):
    return AuthService(settings=settings, auth_repo=auth_repo)


# FIXME - This test is failing because the AuthService is not being mocked correctly
# @pytest.mark.asyncio
# async def test_login_for_access_token(test_client: TestClient, auth_service: AuthService):
#     # Create payload
#     user = UserCreateRequestFactory.build()

#     # Create user
#     response = test_client.post("api/user", json=user.model_dump())

#     # Mock the form data and the expected token
#     form_data = OAuth2PasswordRequestFormDependency(username="testuser", password="testpassword")
#     expected_token = Token(access_token="testtoken", token_type="bearer")

#     # Mock the login_for_access_token method
#     auth_service.login_for_access_token = AsyncMock(return_value=expected_token)

#     # Make the request to the endpoint
#     response = test_client.post(
#         "api/auth/token", data={"username": "testuser", "password": "testpassword"}
#     )

#     # Assert the response
#     assert response.status_code == status.HTTP_200_OK
#     assert response.json() == expected_token.model_dump()

#     # Assert that the login_for_access_token method was called with the correct form data
#     auth_service.login_for_access_token.assert_awaited_once_with(form_data)
