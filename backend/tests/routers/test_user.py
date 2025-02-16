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
