from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_city_get():
    response = client.get("/cities/")
    assert response.status_code == 200
    assert len(response.json()) >= 1

def test_create_city():
    response = client.post("/cities/", json={"name": "Уфа", "mayor_name":"Иванов И.И.", "landmark_photo":"hhh", "id_region": 5})
    assert response.status_code == 200
    assert response.json()["name"] == "Уфа"
