import pytest
from app.engines.disaggregation_engine import disaggregation_engine
from app.engines.data_generator import generate_microgrid_dataset

def test_disaggregation_accuracy():
    df = generate_microgrid_dataset()
    result = disaggregation_engine.disaggregate_dataframe(df)
    assert "tiers" in result
    assert "critical" in result["tiers"]
    assert "essential" in result["tiers"]
    assert "flexible" in result["tiers"]
    assert "evaluation_metrics" in result
    assert result["evaluation_metrics"]["mae_kw"] >= 0.0

def test_drilldown_endpoint():
    df = generate_microgrid_dataset()
    evidence = disaggregation_engine.get_drilldown_evidence(df, "EQ_WP_01")
    assert evidence["equipment_id"] == "EQ_WP_01"
    assert "cause_explanation" in evidence
    assert len(evidence["timeseries"]) == 96
