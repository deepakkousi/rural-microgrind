from app.schemas import (
    EquipmentItem,
    TelemetryRecord,
    DisaggregationSummary,
    CauseEvidence,
    Recommendation,
    FreshnessStatus,
    VerificationSummary,
    FailureSimulationRequest,
    ErrorResponse,
    ErrorDetail
)
from pydantic import BaseModel
from typing import Dict, Any

class HealthResponse(BaseModel):
    status: str
    engine_count: int
    service_count: int
    engines: Dict[str, str]
    services: Dict[str, str]
    timestamp: str
