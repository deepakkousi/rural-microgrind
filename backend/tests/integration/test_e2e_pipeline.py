import pytest
import pandas as pd
from fastapi.testclient import TestClient
from app.main import app
from app.engines.quality_engine import quality_engine
from app.engines.verification_engine import verification_engine
from app.core.config import settings

client = TestClient(app)

@pytest.fixture(autouse=True)
def cleanup_simulations():
    """Ensure every test starts with clean simulated failures."""
    quality_engine.set_simulated_failure(failure_type="RESET")
    yield
    quality_engine.set_simulated_failure(failure_type="RESET")


# -------------------------------------------------------------------------
# Test 1: Full Normal Telemetry Ingestion -> Verification Pipeline Flow
# -------------------------------------------------------------------------
def test_e2e_normal_pipeline():
    """
    End-to-End flow:
    1. Telemetry Ingestion: Check meter records are complete and valid.
    2. Quality Check: Confirm telemetry is LIVE with high reliability.
    3. Disaggregation: Tier breakdown and error evaluation metrics.
    4. Cause Detection: Detect inefficiencies with evidence scoring.
    5. Verification: Compute baseline vs measured and mathematical reconciliation.
    """
    # 1. Freshness / Quality
    fresh_resp = client.get("/api/quality/freshness")
    assert fresh_resp.status_code == 200
    fresh_data = fresh_resp.json()
    assert fresh_data["status"] == "LIVE"
    assert fresh_data["recommendation_reliability"] == "HIGH"

    # 2. Ingestion
    meter_resp = client.get("/api/data/meter?limit=96")
    assert meter_resp.status_code == 200
    records = meter_resp.json()
    assert len(records) == 96
    latest = records[-1]
    assert latest["total_kw"] > 0
    assert "hvac_kw" in latest
    assert "water_pump_kw" in latest

    # 3. Disaggregation
    disagg_resp = client.get("/api/disaggregation")
    assert disagg_resp.status_code == 200
    disagg = disagg_resp.json()
    assert disagg["total_kw"] > 0
    assert "tiers" in disagg
    assert disagg["tiers"]["critical"]["kw"] > 0
    assert disagg["tiers"]["essential"]["kw"] > 0
    assert disagg["tiers"]["flexible"]["kw"] > 0
    assert "mae_kw" in disagg["evaluation_metrics"]
    assert disagg["evaluation_metrics"]["mae_kw"] < 0.5

    # 4. Cause Analysis & Recommendations
    rec_resp = client.get("/api/recommendations")
    assert rec_resp.status_code == 200
    recs = rec_resp.json()
    assert len(recs) >= 2
    for r in recs:
        assert r["evidence_score"] >= 80
        assert r["action_type"] in ["COST_REDUCTION", "ENERGY_REDUCTION"]
        assert len(r["cause"]) > 10
        assert len(r["recommended_action"]) > 10

    # 5. Verification
    verif_resp = client.get("/api/verification/summary")
    assert verif_resp.status_code == 200
    verif = verif_resp.json()
    assert verif["status"] == "AVAILABLE"
    assert verif["baseline_daily_avg_kwh"] > verif["measured_daily_avg_kwh"]
    assert verif["verified_reduction_kwh_day"] > 0
    assert verif["cost_saving_daily"] > 0
    
    # Mathematical reconciliation
    recon = verif["reconciliation"]
    assert recon["main_meter_reduction_kwh_day"] == verif["verified_reduction_kwh_day"]
    assert abs(recon["background_unmetered_variance_kwh_day"]) < 5.0


# -------------------------------------------------------------------------
# Test 2: Missing Telemetry Handling Flow
# -------------------------------------------------------------------------
def test_e2e_missing_telemetry_flow():
    """
    When smart meter data feeds drop (MISSING_DATA):
    - Freshness status drops to MISSING.
    - Reliability is DISABLED.
    - Cause engine suppresses recommendations (empty list).
    - Verification engine returns DATA_UNAVAILABLE on empty inputs.
    - System never crashes with unhandled exceptions.
    """
    client.post("/api/quality/simulate-failure", json={
        "failure_type": "MISSING_DATA",
        "duration_intervals": 16,
        "affected_channel": "water_pump_kw"
    })

    fresh_resp = client.get("/api/quality/freshness")
    assert fresh_resp.status_code == 200
    fresh = fresh_resp.json()
    assert fresh["status"] == "MISSING"
    assert fresh["recommendation_reliability"] == "DISABLED"
    assert "unavailable" in fresh["warning_message"].lower()

    # Recommendations suppressed
    rec_resp = client.get("/api/recommendations")
    assert rec_resp.status_code == 200
    assert rec_resp.json() == []

    # Verification handles missing dataframe gracefully
    empty_res = verification_engine.evaluate_verification_experiment(pd.DataFrame())
    assert empty_res["status"] == "DATA_UNAVAILABLE"


# -------------------------------------------------------------------------
# Test 3: Stale Telemetry Degradation Flow
# -------------------------------------------------------------------------
def test_e2e_stale_telemetry_flow():
    """
    When meter data is delayed / stale (STALE_DATA):
    - Freshness status is STALE.
    - Reliability is DEGRADED.
    - Recommendations are still generated, but evidence scores are penalized (downgraded by 15 points).
    """
    # 1. Baseline evidence scores under LIVE condition
    live_resp = client.get("/api/recommendations")
    assert live_resp.status_code == 200
    live_recs = {r["recommendation_id"]: r["evidence_score"] for r in live_resp.json()}

    # 2. Inject STALE_DATA failure
    client.post("/api/quality/simulate-failure", json={
        "failure_type": "STALE_DATA",
        "duration_intervals": 16,
        "affected_channel": "water_pump_kw"
    })

    fresh_resp = client.get("/api/quality/freshness")
    assert fresh_resp.status_code == 200
    fresh = fresh_resp.json()
    assert fresh["status"] == "STALE"
    assert fresh["recommendation_reliability"] == "DEGRADED"

    # 3. Degraded evidence scores
    stale_resp = client.get("/api/recommendations")
    assert stale_resp.status_code == 200
    stale_recs = {r["recommendation_id"]: r["evidence_score"] for r in stale_resp.json()}

    for rec_id, live_score in live_recs.items():
        assert rec_id in stale_recs
        # Telemetry freshness contribution dropped from 30 to 15 (-15 score)
        assert stale_recs[rec_id] == live_score - 15


# -------------------------------------------------------------------------
# Test 4: Sensor Anomaly Detection and Safe Handling
# -------------------------------------------------------------------------
def test_e2e_sensor_anomaly_handling():
    """
    Inject STUCK_SENSOR anomaly:
    - Anomaly detection identifies sensor flatline.
    - Data ingestion and disaggregation do not fail.
    """
    client.post("/api/quality/simulate-failure", json={
        "failure_type": "STUCK_SENSOR",
        "duration_intervals": 20,
        "affected_channel": "water_pump_kw"
    })

    anom_resp = client.get("/api/quality/anomalies")
    assert anom_resp.status_code == 200
    anomalies = anom_resp.json()
    assert isinstance(anomalies, list)
    assert any("water_pump_kw" in a["sensor"] for a in anomalies)
    assert any(a["issue_type"] == "FLATLINE_STUCK" for a in anomalies)

    # Core endpoints survive without 500 error
    meter_resp = client.get("/api/data/meter?limit=20")
    assert meter_resp.status_code == 200
    disagg_resp = client.get("/api/disaggregation")
    assert disagg_resp.status_code == 200


# -------------------------------------------------------------------------
# Test 5: Dynamic Tariff Recalculation & Energy Separation
# -------------------------------------------------------------------------
def test_e2e_tariff_dynamics_and_separation():
    """
    Verify architectural principle:
    Physical energy reduction (kWh) is strictly separated from financial savings (₹).
    Water pump shift produces 0 kWh energy savings but non-zero cost savings.
    """
    verif_resp = client.get("/api/verification/summary")
    assert verif_resp.status_code == 200
    verif = verif_resp.json()

    interventions = {i["id"]: i for i in verif["interventions_applied"]}
    
    # Water Pump (INT_01) - Load shift only
    wp = interventions["INT_01"]
    assert wp["type"] == "COST_REDUCTION"
    assert wp["energy_saving_kwh_day"] == 0.0 # Strict zero energy reduction
    assert wp["cost_saving_daily_inr"] > 0.0   # True financial savings

    # HVAC (INT_02) - True energy reduction
    hvac = interventions["INT_02"]
    assert hvac["type"] == "ENERGY_REDUCTION"
    assert hvac["energy_saving_kwh_day"] > 0.0 # Real kWh reduction
    assert hvac["cost_saving_daily_inr"] > 0.0


# -------------------------------------------------------------------------
# Test 6: Complete Recommendation Lifecycle & Drilldown Evidence Flow
# -------------------------------------------------------------------------
def test_e2e_recommendation_lifecycle_and_drilldown():
    """
    Inspect recommendation -> examine drilldown evidence -> accept/apply -> verify state change.
    """
    # 1. Fetch recommendations
    recs = client.get("/api/recommendations").json()
    target_rec = recs[0]
    rec_id = target_rec["recommendation_id"]
    eq_id = target_rec["equipment_id"]

    # 2. Drilldown evidence
    drill_resp = client.get(f"/api/disaggregation/drilldown/{eq_id}")
    assert drill_resp.status_code == 200
    drill = drill_resp.json()
    assert drill["equipment_id"] == eq_id
    assert len(drill["timeseries"]) == 96
    assert len(drill["cause_explanation"]) > 20

    # 3. Apply recommendation
    apply_resp = client.post(f"/api/recommendations/{rec_id}/status", json={"status": "APPLIED"})
    assert apply_resp.status_code == 200
    assert apply_resp.json()["status"] == "APPLIED"

    # 4. Verify persistence
    updated_recs = client.get("/api/recommendations").json()
    updated_target = next(r for r in updated_recs if r["recommendation_id"] == rec_id)
    assert updated_target["status"] == "APPLIED"

    # 5. Reset status
    reset_resp = client.post(f"/api/recommendations/{rec_id}/status", json={"status": "PENDING"})
    assert reset_resp.status_code == 200
