from fastapi.testclient import TestClient
from app.main import app, CORE_ENGINES, REGISTERED_SERVICES

client = TestClient(app)

def test_api_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "HEALTHY"
    assert data["engine_count"] == len(CORE_ENGINES)
    assert data["service_count"] == len(REGISTERED_SERVICES)

def test_i18n_translation():
    resp_en = client.get("/api/i18n/en")
    assert resp_en.status_code == 200
    assert "title" in resp_en.json()

    resp_hi = client.get("/api/i18n/hi")
    assert resp_hi.status_code == 200
    assert "ग्रामीण माइक्रोग्रिड" in resp_hi.json()["title"]

def test_role_permissions():
    resp_eq = client.get("/api/equipment")
    assert resp_eq.status_code == 200
    assert len(resp_eq.json()) == 9

    resp_dis = client.get("/api/disaggregation")
    assert resp_dis.status_code == 200
    assert "tiers" in resp_dis.json()
