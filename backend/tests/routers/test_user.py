from backend.tests.factories import UserFactory


def test_create_item(test_client):
    # Create payload
    item = UserFactory.build()

    # Create item
    response = test_client.post("api/user/", json=item.model_dump())

    # Assert response
    assert response.status_code == 201
