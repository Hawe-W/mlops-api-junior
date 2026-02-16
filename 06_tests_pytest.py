from fastapi.testclient import TestClient
from fastapi_simple import app

client = TestClient(app)

def test_predire_ok():
    response = client.post("/predire", json={"donnees": [1, 2, 3]})
    assert response.status_code == 200
    assert response.json()["prediction"] == 3

def test_predire_vide():
    response = client.post("/predire", json={"donnees": []})
    assert response.status_code == 200
    assert response.json()["prediction"] == 0
