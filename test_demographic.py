from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_demographic_get():
    response = client.get("/demographics/")
    assert response.status_code == 200
    assert len(response.json()) >= 1

def test_create_city():
    response = client.post("/demographics/", json={"birth_rate":8.8, "death_rate":6.6, "population":1163304, "id_city":4})
    assert response.status_code == 200
    assert response.json()["id_city"] == 4