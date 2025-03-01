from datetime import timedelta

from fastapi.testclient import TestClient

from backend.common.config import Settings
from backend.features.auth.domain.services import AuthService
from backend.features.user.repositories.sql.entities import UserSqlEntity
from backend.tests.factories import UserFactory


class MockAuthRepository:
    async def get_user_by_username(self, username: str):
        return UserSqlEntity(username=username, email="test@example.com")


# def test_login_for_access_token(test_client: TestClient, db_session, test_settings: Settings):
#     # Create auth service with mock repository
#     auth_repo = MockAuthRepository()
#     auth_service = AuthService(settings=test_settings, auth_repo=auth_repo)

#     # Create a test user in the database
#     user_data = UserFactory.build(username="testuser", password="testpassword")
#     db_session.add(user_data)
#     db_session.commit()

#     # Make a request to the login endpoint
#     response = test_client.post(
#         "api/auth/token",
#         data={"username": "testuser", "password": "testpassword"},
#     )

#     # Assert response
#     assert response.status_code == 200
#     response_data = response.json()
#     assert "access_token" in response_data
#     assert response_data["token_type"] == "bearer"

#     # Verify the access token
#     token = response_data["access_token"]
#     user = auth_service.get_current_user(token=token)
#     assert user.username == "testuser"


def test_protected_route(test_client: TestClient, db_session, test_settings: Settings):
    # Create auth service with mock repository
    auth_repo = MockAuthRepository()
    auth_service = AuthService(settings=test_settings, auth_repo=auth_repo)

    # Create payload
    user_data = UserFactory.build()

    # Create user
    db_session.add(user_data)
    db_session.commit()

    # Create token
    token = auth_service.create_access_token(
        data={"sub": user_data.username},
        expires_delta=timedelta(minutes=30),
    )

    # Get user
    response = test_client.get("api/auth/users/me", headers={"Authorization": f"Bearer {token}"})

    # Assert response
    assert response.status_code == 200
    assert response.json()["username"] == user_data.username


def test_protected_route_no_token(test_client: TestClient):
    # Get user
    response = test_client.get("api/auth/users/me")

    # Assert response
    assert response.status_code == 401
