from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_demographic_get():
    response = client.get("/populations/")
    assert response.status_code == 200
    assert len(response.json()) >= 1

def test_create_city():
    response = client.post("/populations/", json={"year":2024, "population":1163304, "id_city":4})
    assert response.status_code == 200
    assert response.json()["id_city"] == 4