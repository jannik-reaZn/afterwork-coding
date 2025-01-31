from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_example():
    response = client.get("api/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to FastAPI with Conda!"}
