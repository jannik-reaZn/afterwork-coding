import pytest

from backend.tests.factories import UserCreateRequestFactory


def test_create_user(test_client):
    # Create payload
    user_data = UserCreateRequestFactory.build()

    # Create user
    response = test_client.post("api/user", json=user_data.model_dump())

    # Assert response
    assert response.status_code == 201
    assert "username" in response.json()


@pytest.mark.parametrize(
    "invalid_data, expected_error",
    [
        (
            {
                "username": "",
                "email": "valid@example.com",
                "hashed_password": "$2b$12$/jPk8EoQT7PJCAQRuYeX9eO7m8sBO9Im5/wme2MDf.FnF7j5v/jO2'",
            },
            "username",
        ),
        (
            {
                "username": "john doe",
                "email": "",
                "hashed_password": "$2b$12$/jPk8EoQT7PJCAQRuYeX9eO7m8sBO9Im5/wme2MDf.FnF7j5v/jO2'",
            },
            "email",
        ),
        (
            {"username": "john doe", "email": "valid@example.com", "hashed_password": ""},
            "hashed_password",
        ),
    ],
)
def test_create_user_with_invalid_data(test_client, invalid_data, expected_error):
    # NOTE: The factory cannot be used to create invalid data because pydantic would throw a
    # ValidationError. That is why the factory is used to create valid data first, and then
    # invalid data is set individually.

    # Create payload
    invalid_user_data = UserCreateRequestFactory.build()
    invalid_user_data.user_create.username = invalid_data["username"]
    invalid_user_data.user_create.email = invalid_data["email"]
    invalid_user_data.user_create.hashed_password = invalid_data["hashed_password"]

    # Create user
    response = test_client.post("api/user", json=invalid_user_data.model_dump())

    # Assert response
    assert response.status_code == 422  # Expecting Unprocessable Entity


def test_get_user(test_client):
    # Create payload
    user = UserCreateRequestFactory.build()

    # Create user
    response = test_client.post("api/user", json=user.model_dump())

    # Get user
    response = test_client.get(f"api/user/{user.user_create.id}")

    # Assert response
    assert response.status_code == 200
    assert response.json()["id"] == user.user_create.id
    assert response.json()["username"] == user.user_create.username
    assert response.json()["email"] == user.user_create.email


def test_get_user_not_found(test_client):
    from fastapi.exceptions import ResponseValidationError

    # Get user and assert ResponseValidationError is raised
    with pytest.raises(ResponseValidationError):
        test_client.get("api/user/100")


def test_delete_user(test_client):
    # Create payload
    user = UserCreateRequestFactory.build()

    # Create user
    response = test_client.post("api/user", json=user.model_dump())

    # Delete user
    response = test_client.delete(f"api/user/{user.user_create.id}")

    # Assert response
    assert response.status_code == 204


def test_delete_user_not_found(test_client):
    # Delete user
    response = test_client.delete("api/user/100")

    # Assert response
    assert response.status_code == 204
