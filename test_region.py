from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_region_get():
    response = client.get("/regions/")
    assert response.status_code == 200
    assert len(response.json()) >= 1

def test_create_region():
    response = client.post("/regions/", json={"name": "Республика Башкортостан", "number": 2, "id_district": 2})
    assert response.status_code == 200
    assert response.json()["name"] == "Республика Башкортостан"
