from backend.tests.factories.item import ItemFactory


def test_create_item(test_client):
    # Create payload
    item = ItemFactory.build()

    # Create item
    response = test_client.post("api/items/", json=item.model_dump())

    # Assert response
    assert response.status_code == 201


def test_read_item(test_client):
    # Create payload
    item = ItemFactory.build()

    # Create item
    create_response = test_client.post("api/items/", json=item.model_dump())
    assert create_response.status_code == 201
    created_item = create_response.json()

    # Read created item
    response = test_client.get(f"api/items/{created_item['id']}")
    assert response.status_code == 200


def test_read_item_not_found(test_client):
    response = test_client.get("api/items/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"
