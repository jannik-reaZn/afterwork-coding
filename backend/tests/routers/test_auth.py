from datetime import timedelta

from backend.features.auth.domain.services import AuthService
from backend.features.user.repositories.entity.user_entity import User
from backend.tests.factories import UserFactory


class MockAuthRepository:
    async def get_user_by_username(self, username: str):
        return User(username=username, email="test@example.com")


def test_protected_route(test_client, db_session, test_settings):
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


def test_protected_route_no_token(test_client):
    # Get user
    response = test_client.get("api/auth/users/me")

    # Assert response
    assert response.status_code == 401
