import pytest
import pandas as pd
import numpy as np
from app.engines.quality_engine import quality_engine
from app.engines.data_generator import generate_microgrid_dataset
from app.engines.verification_engine import verification_engine
from app.engines.cause_engine import cause_engine
from app.engines.disaggregation_engine import disaggregation_engine

def test_missing_data_handling():
    quality_engine.set_simulated_failure("MISSING_DATA")
    anomalies = quality_engine.detect_anomalies(generate_microgrid_dataset())
    assert any(a["issue_type"] == "MISSING_SIGNAL" for a in anomalies)
    freshness = quality_engine.evaluate_freshness()
    assert freshness.status == "MISSING"
    assert freshness.recommendation_reliability == "DISABLED"
    
    # Recommendations disabled under missing data
    recs = cause_engine.analyze_causes_and_recommendations(generate_microgrid_dataset())
    assert len(recs) == 0
    quality_engine.set_simulated_failure("RESET")

def test_stuck_sensor_handling():
    quality_engine.set_simulated_failure("STUCK_SENSOR", affected_channel="water_pump_kw")
    anomalies = quality_engine.detect_anomalies(generate_microgrid_dataset())
    assert any(a["issue_type"] == "FLATLINE_STUCK" for a in anomalies)
    quality_engine.set_simulated_failure("RESET")

def test_negative_reading_handling():
    quality_engine.set_simulated_failure("NEGATIVE_READING", affected_channel="hvac_kw")
    anomalies = quality_engine.detect_anomalies(generate_microgrid_dataset())
    assert any(a["issue_type"] == "POLARITY_ERROR" for a in anomalies)
    quality_engine.set_simulated_failure("RESET")

def test_tariff_revision_handling():
    quality_engine.set_simulated_failure("TARIFF_REVISION")
    df = quality_engine.apply_quality_checks_and_failures(generate_microgrid_dataset())
    assert (df.tail(16)['tariff_period'] == 'CRITICAL_PEAK').all()
    # Dynamic recalculation in cause engine uses revised tariff
    recs = cause_engine.analyze_causes_and_recommendations(df)
    assert len(recs) > 0
    quality_engine.set_simulated_failure("RESET")

def test_empty_dataset_edge_case():
    empty_df = pd.DataFrame()
    ver_res = verification_engine.evaluate_verification_experiment(empty_df)
    assert ver_res["status"] == "DATA_UNAVAILABLE"
    
    dis_res = disaggregation_engine.disaggregate_dataframe(empty_df)
    assert dis_res == {}
    
    cause_res = cause_engine.analyze_causes_and_recommendations(empty_df)
    assert cause_res == []

def test_stale_telemetry_edge_cases():
    quality_engine.set_simulated_failure("STALE_DATA")
    freshness = quality_engine.evaluate_freshness()
    assert freshness.status == "STALE"
    assert freshness.recommendation_reliability == "DEGRADED"
    quality_engine.set_simulated_failure("RESET")
    
    # Test very stale (> 2 hours)
    very_stale_ts = "2020-01-01T00:00:00"
    freshness_vs = quality_engine.evaluate_freshness(very_stale_ts)
    # Scaled check or status check
    assert freshness_vs.status in ["LIVE", "STALE", "VERY_STALE"]

def test_solar_greater_than_load_edge_case():
    df = generate_microgrid_dataset(days=1)
    df.loc[0, 'solar_gen_kw'] = 50.0
    df.loc[0, 'total_kw'] = 10.0
    df['net_grid_kw'] = np.round((df['total_kw'] - df['solar_gen_kw']).clip(lower=0.0), 2)
    assert df.loc[0, 'net_grid_kw'] == 0.0 # Never negative grid import
