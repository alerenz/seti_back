from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_district():
    response = client.post("/districts/", json={"name": "New District"})
    assert response.status_code == 200
    assert response.json()["name"] == "New District"

def test_region_get():
    response = client.get("/districts/")
    assert response.status_code == 200
    assert len(response.json()) >= 1



