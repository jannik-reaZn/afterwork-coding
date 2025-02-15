from datetime import timedelta

from backend.features.auth.domain.services import create_access_token
from backend.features.user.repositories.entity.user_entity import User
from backend.tests.factories import UserFactory


def test_create_user(test_client):
    # Create payload
    user_data = UserFactory.build()
    user_data.hashed_password = User.hash_password("testpassword")

    # Create user
    response = test_client.post("api/user", json=user_data.model_dump())

    # Assert response
    assert response.status_code == 201
    assert "username" in response.json()


def test_protected_route(test_client, db_session, test_settings):
    # Create payload
    user_data = UserFactory.build()

    # Create user
    db_session.add(user_data)
    db_session.commit()

    # Create token
    token = create_access_token(
        settings=test_settings,
        data={"sub": user_data.username},
        expires_delta=timedelta(minutes=30),
    )

    # Get user
    response = test_client.get("api/user/users/me", headers={"Authorization": f"Bearer {token}"})

    # Assert response
    assert response.status_code == 200
    assert response.json()["username"] == user_data.username


def test_protected_route_no_token(test_client):
    # Get user
    response = test_client.get("api/user/users/me")

    # Assert response
    assert response.status_code == 401
