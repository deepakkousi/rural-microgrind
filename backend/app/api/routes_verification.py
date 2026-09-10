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
