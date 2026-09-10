import pytest
from app.engines.quality_engine import quality_engine
from app.engines.data_generator import generate_microgrid_dataset

def test_freshness_classification():
    quality_engine.set_simulated_failure("RESET")
    freshness = quality_engine.evaluate_freshness()
    assert freshness.status == "LIVE"
    assert freshness.recommendation_reliability == "HIGH"

def test_missing_data_classification():
    quality_engine.set_simulated_failure("MISSING_DATA")
    freshness = quality_engine.evaluate_freshness()
    assert freshness.status == "MISSING"
    assert freshness.recommendation_reliability == "DISABLED"
    quality_engine.set_simulated_failure("RESET")

def test_stale_data_classification():
    quality_engine.set_simulated_failure("STALE_DATA")
    freshness = quality_engine.evaluate_freshness()
    assert freshness.status == "STALE"
    assert freshness.recommendation_reliability == "DEGRADED"
    quality_engine.set_simulated_failure("RESET")
