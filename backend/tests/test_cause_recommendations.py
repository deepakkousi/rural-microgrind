import pytest
from app.engines.cause_engine import cause_engine
from app.engines.recommendation_engine import recommendation_manager
from app.engines.data_generator import generate_microgrid_dataset
from app.engines.quality_engine import quality_engine

def test_cause_detection():
    quality_engine.set_simulated_failure("RESET")
    df = generate_microgrid_dataset()
    recs = cause_engine.analyze_causes_and_recommendations(df)
    assert len(recs) >= 2
    rec_ids = [r.recommendation_id for r in recs]
    assert "REC_WP_01" in rec_ids and "REC_HVAC_01" in rec_ids

def test_recommendations_evidence_score_and_action_type():
    df = generate_microgrid_dataset()
    recs = recommendation_manager.get_all_recommendations(df)
    for r in recs:
        assert r.estimated_cost_saving > 0.0
        assert 0 <= r.evidence_score <= 100
        assert r.confidence == round(r.evidence_score / 100.0, 2)
        assert len(r.evidence_breakdown) > 0
        assert r.status in ["PENDING", "APPLIED", "REJECTED"]
        
        # Verify action_type classification
        if r.recommendation_id in ["REC_WP_01", "REC_LAB_01"]:
            assert r.action_type == "COST_REDUCTION"
            assert r.estimated_energy_saving_kwh == 0.0 # Pure load shift
        elif r.recommendation_id == "REC_HVAC_01":
            assert r.action_type == "ENERGY_REDUCTION"
            assert r.estimated_energy_saving_kwh > 0.0 # Genuine energy reduction

def test_explainability_non_technical():
    df = generate_microgrid_dataset()
    recs = recommendation_manager.get_all_recommendations(df)
    for r in recs:
        assert len(r.problem) > 10
        assert len(r.cause) > 10
        assert len(r.recommended_action) > 10
        # Should not contain raw jargon without explanation
        assert "Anomaly score" not in r.cause

def test_status_transition():
    recommendation_manager.update_recommendation_status("REC_WP_01", "APPLIED")
    assert recommendation_manager.applied_status["REC_WP_01"] == "APPLIED"
    recommendation_manager.update_recommendation_status("REC_WP_01", "PENDING")
