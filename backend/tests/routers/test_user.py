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
    # Create payload
    custom_fields = {
        "user_create__id": 100,
        "user_create__username": invalid_data["username"],
        "user_create__email": invalid_data["email"],
        "user_create__hashed_password": invalid_data["hashed_password"],
    }
    invalid_user_data = UserCreateRequestFactory.build(**custom_fields)

    # Create user
    response = test_client.post("api/user", json=invalid_user_data.model_dump())

    # Assert response
    assert response.status_code == 422
    assert response.json() == {
        "title": "ValidationError",
        "description": (
            "The server was unable to process the request, because it contains invalid data."
        ),
        "code": 422,
    }
