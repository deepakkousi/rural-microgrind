import pytest
from app.engines.quality_engine import quality_engine
from app.engines.data_generator import generate_microgrid_dataset

def test_missing_data_handling():
    quality_engine.set_simulated_failure("MISSING_DATA")
    anomalies = quality_engine.detect_anomalies(generate_microgrid_dataset())
    assert any(a["issue_type"] == "MISSING_SIGNAL" for a in anomalies)
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
    quality_engine.set_simulated_failure("RESET")
