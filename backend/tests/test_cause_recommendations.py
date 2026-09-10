import pytest
from app.engines.cause_engine import cause_engine
from app.engines.recommendation_engine import recommendation_manager
from app.engines.data_generator import generate_microgrid_dataset
from app.engines.quality_engine import quality_engine

def test_cause_detection():
    quality_engine.set_simulated_failure("RESET")
    df = generate_microgrid_dataset()
    recs = cause_engine.analyze_causes_and_recommendations(df)
    assert len(recs) >= 2 # Should detect water pump peak tariff & HVAC low occupancy causes
    rec_ids = [r.recommendation_id for r in recs]
    assert "REC_WP_01" in rec_ids or "REC_HVAC_01" in rec_ids

def test_recommendations_generation():
    df = generate_microgrid_dataset()
    recs = recommendation_manager.get_all_recommendations(df)
    for r in recs:
        assert r.estimated_energy_saving_kwh > 0
        assert r.estimated_cost_saving > 0
        assert r.confidence > 0.5
        assert r.status in ["PENDING", "APPLIED", "REJECTED"]

def test_explainability():
    df = generate_microgrid_dataset()
    recs = recommendation_manager.get_all_recommendations(df)
    for r in recs:
        assert len(r.problem) > 10
        assert len(r.cause) > 10
        assert len(r.recommended_action) > 10
