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
def simulate_edge_failure(
    request: FailureSimulationRequest = None,
    failure_type: str = None,
    duration_intervals: int = 16,
    affected_channel: str = "water_pump_kw"
):
    ft = (request.failure_type if request and request.failure_type else failure_type) or "RESET"
    dur = (request.duration_intervals if request and request.duration_intervals else duration_intervals) or 16
    aff = (request.affected_channel if request and request.affected_channel else affected_channel) or "water_pump_kw"

    quality_engine.set_simulated_failure(
        failure_type=ft,
        duration_intervals=dur,
        affected_channel=aff
    )
    return {
        "status": "SIMULATION_UPDATED",
        "failure_type": ft,
        "affected_channel": aff
    }
