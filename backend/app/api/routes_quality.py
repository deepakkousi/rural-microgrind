from fastapi import APIRouter
from app.engines.quality_engine import quality_engine
from app.core.schemas import FailureSimulationRequest
from app.api.routes_data import get_current_df

router = APIRouter(prefix="/quality", tags=["Data Quality & Freshness"])

@router.get("/freshness")
def get_freshness_status():
    df = get_current_df()
    latest_ts = df.iloc[-1]['timestamp'] if not df.empty and 'timestamp' in df.columns else None
    return quality_engine.evaluate_freshness(latest_ts)

@router.get("/anomalies")
def get_sensor_anomalies():
    df = get_current_df()
    return quality_engine.detect_anomalies(df)

@router.post("/simulate-failure")
def simulate_edge_failure(request: FailureSimulationRequest):
    quality_engine.set_simulated_failure(
        failure_type=request.failure_type,
        duration_intervals=request.duration_intervals,
        affected_channel=request.affected_channel or "water_pump_kw"
    )
    return {
        "status": "SIMULATION_UPDATED",
        "failure_type": request.failure_type,
        "affected_channel": request.affected_channel
    }
