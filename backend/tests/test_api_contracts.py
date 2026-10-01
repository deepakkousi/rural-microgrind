import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# ---------------------------------------------------------
# 1. Standard Success Contract Tests (200 OK & Schema Valid)
# ---------------------------------------------------------

def test_health_contract():
    resp = client.get("/api/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "HEALTHY"
    assert "engine_count" in data
    assert "service_count" in data
    assert isinstance(data["engines"], dict)
    assert isinstance(data["services"], dict)
    assert "timestamp" in data


def test_data_meter_contract_valid():
    resp = client.get("/api/data/meter?limit=10")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) == 10
    record = data[0]
    expected_keys = [
        "timestamp", "total_kw", "it_network_kw", "lighting_kw",
        "water_pump_kw", "kitchen_kw", "hvac_kw", "lab_equipment_kw",
        "occupancy", "tariff_period", "tariff_rate", "solar_gen_kw",
        "net_grid_kw"
    ]
    for key in expected_keys:
        assert key in record, f"Missing key {key} in meter record"


def test_data_context_contract_valid():
    resp = client.get("/api/data/context?limit=5")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) == 5
    for key in ["timestamp", "occupancy", "tariff_period", "tariff_rate", "solar_gen_kw"]:
        assert key in data[0]


def test_data_summary_contract():
    resp = client.get("/api/data/summary")
    assert resp.status_code == 200
    data = resp.json()
    assert "total_records" in data
    assert data["total_records"] > 0
    assert "latest_record" in data
    assert "date_range" in data
    assert "start" in data["date_range"]
    assert "end" in data["date_range"]


def test_disaggregation_contract():
    resp = client.get("/api/disaggregation")
    assert resp.status_code == 200
    data = resp.json()
    assert "timestamp" in data
    assert "total_kw" in data
    assert "tiers" in data
    assert "critical" in data["tiers"]
    assert "essential" in data["tiers"]
    assert "flexible" in data["tiers"]
    assert "evaluation_metrics" in data
    assert "mae_kw" in data["evaluation_metrics"]
    assert "rmse_kw" in data["evaluation_metrics"]
    assert "detailed_loads" in data
    assert isinstance(data["detailed_loads"], list)


def test_drilldown_contract_valid():
    resp = client.get("/api/disaggregation/drilldown/EQ_WP_01")
    assert resp.status_code == 200
    data = resp.json()
    assert data["equipment_id"] == "EQ_WP_01"
    assert "timeseries" in data
    assert isinstance(data["timeseries"], list)
    assert len(data["timeseries"]) > 0
    point = data["timeseries"][0]
    assert "timestamp" in point
    assert "actual_kw" in point
    assert "expected_kw" in point


def test_recommendations_contract():
    resp = client.get("/api/recommendations")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) > 0
    rec = data[0]
    required_fields = [
        "recommendation_id", "equipment_id", "equipment_name", "load_tier",
        "action_type", "problem", "cause", "evidence",
        "recommended_action", "estimated_energy_saving_kwh", "estimated_cost_saving",
        "evidence_score", "evidence_breakdown", "confidence", "status"
    ]
    for field in required_fields:
        assert field in rec, f"Missing {field} in recommendation"
    assert 0.0 <= rec["confidence"] <= 1.0
    assert 0 <= rec["evidence_score"] <= 100


def test_verification_summary_contract():
    resp = client.get("/api/verification/summary")
    assert resp.status_code == 200
    data = resp.json()
    assert "status" in data
    assert data["status"] == "AVAILABLE"
    assert "baseline_daily_avg_kwh" in data
    assert "measured_daily_avg_kwh" in data
    assert "verified_reduction_kwh_day" in data
    assert "verified_reduction_pct" in data
    assert "cost_saving_daily" in data
    assert "interventions_applied" in data
    assert "reconciliation" in data
    assert isinstance(data["interventions_applied"], list)
    assert "background_unmetered_variance_kwh_day" in data["reconciliation"]


def test_equipment_contract():
    resp = client.get("/api/equipment")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) > 0
    item = data[0]
    assert "equipment_id" in item
    assert "equipment_name" in item
    assert "load_tier" in item
    assert "rated_power_kw" in item


def test_single_equipment_contract():
    resp = client.get("/api/equipment/EQ_WP_01")
    assert resp.status_code == 200
    data = resp.json()
    assert data["equipment_id"] == "EQ_WP_01"
    assert data["load_tier"] == "Essential"
    assert data["rated_power_kw"] == 7.5


def test_quality_freshness_contract():
    resp = client.get("/api/quality/freshness")
    assert resp.status_code == 200
    data = resp.json()
    assert "status" in data
    assert data["status"] in ["LIVE", "STALE", "VERY_STALE", "MISSING"]
    assert "last_updated" in data
    assert "recommendation_reliability" in data


# ---------------------------------------------------------
# 2. Schema Validation & Out-of-Range Tests (422 Envelope)
# ---------------------------------------------------------

def test_validation_error_limit_zero():
    resp = client.get("/api/data/meter?limit=0")
    assert resp.status_code == 422
    data = resp.json()
    assert "error" in data
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert "message" in data["error"]
    assert "details" in data["error"]
    assert "timestamp" in data["error"]
    assert "validation_errors" in data["error"]["details"]
    assert "detail" in data


def test_validation_error_limit_exceeds_max():
    resp = client.get("/api/data/meter?limit=99999")
    assert resp.status_code == 422
    data = resp.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"


def test_validation_error_limit_non_integer():
    resp = client.get("/api/data/meter?limit=abc")
    assert resp.status_code == 422
    data = resp.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"


# ---------------------------------------------------------
# 3. Resource Not Found Tests (404 Envelope)
# ---------------------------------------------------------

def test_resource_not_found_equipment():
    resp = client.get("/api/equipment/EQ_UNKNOWN_NONEXISTENT")
    assert resp.status_code == 404
    data = resp.json()
    assert "error" in data
    assert data["error"]["code"] == "RESOURCE_NOT_FOUND"
    assert "EQ_UNKNOWN_NONEXISTENT" in data["error"]["message"]
    assert "timestamp" in data["error"]
    assert "detail" in data


def test_resource_not_found_drilldown():
    resp = client.get("/api/disaggregation/drilldown/nonexistent_channel_xyz")
    assert resp.status_code == 404
    data = resp.json()
    assert data["error"]["code"] == "RESOURCE_NOT_FOUND"
    assert "nonexistent_channel_xyz" in data["error"]["message"]


# ---------------------------------------------------------
# 4. Invalid Request Payload Tests (400 Envelope)
# ---------------------------------------------------------

def test_invalid_request_missing_status():
    resp = client.post("/api/recommendations/REC_WP_01/status", json={})
    assert resp.status_code == 400
    data = resp.json()
    assert "error" in data
    assert data["error"]["code"] == "INVALID_REQUEST"
    assert "Status field is required" in data["error"]["message"]


def test_invalid_request_bad_status_value():
    resp = client.post("/api/recommendations/REC_WP_01/status", json={"status": "INVALID_STATE"})
    assert resp.status_code == 400
    data = resp.json()
    assert data["error"]["code"] == "INVALID_REQUEST"
    assert "Invalid recommendation status" in data["error"]["message"]


def test_valid_request_status_update():
    resp = client.post("/api/recommendations/REC_WP_01/status", json={"status": "APPLIED"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert data["status"] == "APPLIED"


# ---------------------------------------------------------
# 5. Authoritative Route Parity & Consistency Tests
# ---------------------------------------------------------

def test_tariff_endpoint_contract():
    resp = client.get("/api/data/tariff")
    assert resp.status_code == 200
    data = resp.json()
    assert "currency" in data
    assert "rates" in data
    assert "periods" in data
    assert len(data["periods"]) == 3


def test_causes_endpoint_contract():
    resp = client.get("/api/recommendations/causes")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) >= 2


def test_user_roles_contract():
    resp = client.get("/api/user/roles")
    assert resp.status_code == 200
    data = resp.json()
    assert "roles" in data
    assert len(data["roles"]) == 4

    resp_singular = client.get("/api/user/role")
    assert resp_singular.status_code == 200


def test_verification_baseline_contract():
    resp = client.get("/api/verification/baseline")
    assert resp.status_code == 200
    data = resp.json()
    assert "baseline_period" in data
    assert "baseline_daily_avg_kwh" in data


def test_verification_experiment_contract():
    resp = client.get("/api/verification/experiment")
    assert resp.status_code == 200
    data = resp.json()
    assert "intervention_period" in data
    assert "interventions_applied" in data


def test_openapi_urls_contract():
    assert client.get("/api/openapi.json").status_code == 200
    assert client.get("/api/v1/openapi.json").status_code == 200


def test_recommendation_daily_monthly_consistency():
    resp = client.get("/api/recommendations")
    assert resp.status_code == 200
    for rec in resp.json():
        assert "daily_energy_saving_kwh" in rec
        assert "daily_cost_saving" in rec
        assert "estimated_energy_saving_kwh" in rec
        assert "estimated_cost_saving" in rec
        expected_monthly_kwh = round(rec["daily_energy_saving_kwh"] * 30.0, 1)
        expected_monthly_cost = round(rec["daily_cost_saving"] * 30.0, 2)
        assert rec["estimated_energy_saving_kwh"] == expected_monthly_kwh
        assert rec["estimated_cost_saving"] == expected_monthly_cost

