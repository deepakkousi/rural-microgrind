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
    metrics = result["evaluation_metrics"]
    assert "mae_kw" in metrics
    assert "rmse_kw" in metrics
    assert "mape_pct" in metrics
    assert "wape_pct" in metrics
    
    # Real metrics derived from synthetic Gaussian noise (sigma=0.3)
    assert 0.1 <= metrics["mae_kw"] <= 0.5
    assert 0.1 <= metrics["rmse_kw"] <= 0.6
    assert 0.5 <= metrics["wape_pct"] <= 5.0

def test_drilldown_endpoint():
    df = generate_microgrid_dataset()
    evidence = disaggregation_engine.get_drilldown_evidence(df, "EQ_WP_01")
    assert evidence["equipment_id"] == "EQ_WP_01"
    assert evidence["impact_type"] == "COST_REDUCTION"
    assert "cause_explanation" in evidence
    assert "Water pumping operates during the peak evening electricity tariff" in evidence["cause_explanation"]
    assert len(evidence["timeseries"]) == 96
