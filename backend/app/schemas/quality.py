from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class FreshnessStatus(BaseModel):
    status: str = Field(..., description="Freshness tier (LIVE, STALE, VERY_STALE, MISSING)")
    last_updated: str = Field(..., description="Timestamp of most recent meter reading or N/A")
    age_minutes: float = Field(..., description="Age of data in minutes")
    affected_sources: List[str] = Field(default_factory=list, description="Downstream services impacted")
    recommendation_reliability: str = Field(..., description="Status (HIGH, MEDIUM, LOW, DISABLED)")
    warning_message: Optional[str] = None

class AnomalyItem(BaseModel):
    sensor: str
    issue_type: str # MISSING_SIGNAL, FLATLINE_STUCK, POLARITY_ERROR, STALE_TELEMETRY
    severity: str # CRITICAL, HIGH, MEDIUM, LOW
    description: str
    recommended_action: str

class FailureSimulationRequest(BaseModel):
    failure_type: Optional[str] = Field("RESET", description="MISSING_DATA, STALE_DATA, STUCK_SENSOR, NEGATIVE_READING, TARIFF_REVISION, RESET")
    duration_intervals: Optional[int] = Field(16, description="Duration in 15-min intervals (~4 hours)")
    affected_channel: Optional[str] = Field("water_pump_kw", description="Channel key to affect")

class FailureSimulationResponse(BaseModel):
    status: str
    failure_type: str
    affected_channel: Optional[str] = None
