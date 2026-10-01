from fastapi import APIRouter
from app.engines.verification_engine import verification_engine
from app.api.routes_data import get_current_df

router = APIRouter(prefix="/verification", tags=["Baseline & Experiment Verification"])

@router.get("/summary")
def get_verification_summary():
    df = get_current_df()
    return verification_engine.evaluate_verification_experiment(df)

@router.get("/timeseries")
def get_verification_timeseries():
    df = get_current_df()
    return verification_engine.get_timeseries_comparison(df)

@router.get("/baseline")
def get_baseline_summary():
    df = get_current_df()
    res = verification_engine.evaluate_verification_experiment(df)
    return {
        "status": res.get("status", "AVAILABLE"),
        "baseline_period": res.get("baseline_period"),
        "baseline_daily_avg_kwh": res.get("baseline_daily_avg_kwh"),
        "target_daily_avg_kwh": res.get("target_daily_avg_kwh")
    }

@router.get("/experiment")
def get_experiment_interventions():
    df = get_current_df()
    res = verification_engine.evaluate_verification_experiment(df)
    return {
        "status": res.get("status", "AVAILABLE"),
        "intervention_period": res.get("intervention_period"),
        "verification_period": res.get("verification_period"),
        "interventions_applied": res.get("interventions_applied", [])
    }
