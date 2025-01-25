def test_create_item(test_client, item_payload):
    response = test_client.post("/items/", json=item_payload)
    data = response.json()
    assert response.status_code == 201
    assert data["name"] == "Test Item"
    assert data["price"] == 10.99


def test_read_item(test_client, item_payload):
    # Create item
    create_response = test_client.post("/items/", json=item_payload)
    assert create_response.status_code == 201
    created_item = create_response.json()

    # Read created item
    response = test_client.get(f"/items/{created_item['id']}")
    data = response.json()
    assert response.status_code == 200
    assert data["id"] == created_item["id"]
    assert data["name"] == created_item["name"]
    assert data["price"] == created_item["price"]


def test_read_item_not_found(test_client):
    response = test_client.get("/items/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"
