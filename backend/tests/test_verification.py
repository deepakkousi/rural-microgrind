import pytest
import pandas as pd
from app.engines.verification_engine import verification_engine
from app.engines.data_generator import generate_microgrid_dataset

def test_empty_dataframe_verification():
    summary = verification_engine.evaluate_verification_experiment(pd.DataFrame())
    assert summary["status"] == "DATA_UNAVAILABLE"
    assert "missing" in summary["message"].lower()

def test_baseline_and_target_verification():
    df = generate_microgrid_dataset()
    summary = verification_engine.evaluate_verification_experiment(df)
    assert summary["status"] == "AVAILABLE"
    assert summary["baseline_daily_avg_kwh"] > 0
    assert summary["target_daily_avg_kwh"] < summary["baseline_daily_avg_kwh"]
    assert summary["measured_daily_avg_kwh"] > 0
    assert summary["verified_reduction_kwh_day"] >= 0

def test_energy_vs_cost_reduction_distinction():
    df = generate_microgrid_dataset()
    summary = verification_engine.evaluate_verification_experiment(df)
    interventions = summary["interventions_applied"]
    
    # Water Pump (INT_01) is COST_REDUCTION
    wp_int = next(i for i in interventions if i["id"] == "INT_01")
    assert wp_int["type"] == "COST_REDUCTION"
    assert wp_int["energy_saving_kwh_day"] == 0.0
    assert wp_int["cost_saving_daily_inr"] > 0
    
    # HVAC (INT_02) is ENERGY_REDUCTION
    hvac_int = next(i for i in interventions if i["id"] == "INT_02")
    assert hvac_int["type"] == "ENERGY_REDUCTION"
    assert hvac_int["energy_saving_kwh_day"] > 0
    assert hvac_int["cost_saving_daily_inr"] > 0

def test_error_analysis():
    df = generate_microgrid_dataset()
    summary = verification_engine.evaluate_verification_experiment(df)
    err = summary["error_analysis"]
    assert "absolute_error_kwh" in err
    assert "percentage_error" in err
    assert err["percentage_error"] >= 0.0
    assert "Assumed sensor uncertainty" in err["sensor_uncertainty"]
