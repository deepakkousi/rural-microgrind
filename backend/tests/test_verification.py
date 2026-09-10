import pytest
from app.engines.verification_engine import verification_engine
from app.engines.data_generator import generate_microgrid_dataset

def test_baseline_model():
    df = generate_microgrid_dataset()
    summary = verification_engine.evaluate_verification_experiment(df)
    assert summary.baseline_daily_avg_kwh > 0
    assert summary.measured_daily_avg_kwh > 0

def test_intervention_experiment():
    df = generate_microgrid_dataset()
    summary = verification_engine.evaluate_verification_experiment(df)
    assert len(summary.interventions_applied) == 3

def test_verified_reduction():
    df = generate_microgrid_dataset()
    summary = verification_engine.evaluate_verification_experiment(df)
    assert summary.verified_reduction_kwh_day > 0
    assert summary.verified_reduction_pct > 0
    assert summary.cost_saving_daily > 0

def test_error_analysis():
    df = generate_microgrid_dataset()
    summary = verification_engine.evaluate_verification_experiment(df)
    assert summary.lower_bound_kwh <= summary.verified_reduction_kwh_day <= summary.upper_bound_kwh
    assert summary.measurement_error_margin_pct == 1.8
