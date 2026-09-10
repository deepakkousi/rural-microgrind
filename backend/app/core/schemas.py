from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class EquipmentItem(BaseModel):
    equipment_id: str
    equipment_name: str
    load_tier: str # Critical, Essential, Flexible
    rated_power_kw: float
    location: str
    schedule_description: str
    is_essential: bool
    channel_key: str

class TelemetryRecord(BaseModel):
    timestamp: str
    total_kw: float
    lighting_kw: float
    hvac_kw: float
    water_pump_kw: float
    lab_equipment_kw: float
    kitchen_kw: float
    it_network_kw: float
    solar_gen_kw: float
    occupancy: float
    tariff_period: str
    tariff_rate: float
    net_grid_kw: float

class DisaggregationSummary(BaseModel):
    timestamp: str
    total_kw: float
    components: Dict[str, float]
    percentage_breakdown: Dict[str, float]
    essential_kw: float
    flexible_kw: float
    critical_kw: float
    evaluation: Dict[str, float] # MAE, RMSE, MAPE, WAPE

class CauseEvidence(BaseModel):
    metric: str
    observed_value: float
    expected_value: float
    context: str

class Recommendation(BaseModel):
    recommendation_id: str
    equipment_id: str
    equipment_name: str
    load_tier: str
    action_type: str = "COST_REDUCTION" # COST_REDUCTION (LOAD SHIFT) or ENERGY_REDUCTION
    problem: str
    cause: str
    evidence: CauseEvidence
    recommended_action: str
    estimated_energy_saving_kwh: float # 0.0 for pure load shifts
    estimated_cost_saving: float
    evidence_score: int = 90 # 0 - 100 measurable score
    evidence_breakdown: Dict[str, int] = {}
    confidence: float # legacy compatibility 0.0 to 1.0 (evidence_score / 100.0)
    data_freshness: str # LIVE, STALE, VERY_STALE, MISSING
    priority: str # HIGH, MEDIUM, LOW
    status: str # PENDING, APPLIED, REJECTED

class FreshnessStatus(BaseModel):
    status: str # LIVE, STALE, VERY_STALE, MISSING
    last_updated: str
    age_minutes: float
    affected_sources: List[str]
    recommendation_reliability: str
    warning_message: Optional[str] = None

class VerificationSummary(BaseModel):
    status: str = "AVAILABLE" # AVAILABLE or DATA_UNAVAILABLE
    message: Optional[str] = None
    baseline_period: Optional[str] = None
    intervention_period: Optional[str] = None
    verification_period: Optional[str] = None
    baseline_daily_avg_kwh: Optional[float] = None
    target_daily_avg_kwh: Optional[float] = None
    measured_daily_avg_kwh: Optional[float] = None
    verified_reduction_kwh_day: Optional[float] = None
    verified_reduction_pct: Optional[float] = None
    cost_saving_daily: Optional[float] = None
    cost_saving_total: Optional[float] = None
    target_achievement_pct: Optional[float] = None
    error_analysis: Optional[Dict[str, Any]] = None
    interventions_applied: Optional[List[Dict[str, Any]]] = None
    reconciliation: Optional[Dict[str, Any]] = None

class FailureSimulationRequest(BaseModel):
    failure_type: Optional[str] = "RESET" # MISSING_DATA, STALE_DATA, STUCK_SENSOR, NEGATIVE_READING, TARIFF_REVISION, RESET
    duration_intervals: Optional[int] = 16 # Default ~4 hours
    affected_channel: Optional[str] = "water_pump_kw"

class HealthResponse(BaseModel):
    status: str
    engine_count: int
    service_count: int
    engines: Dict[str, str]
    services: Dict[str, str]
    timestamp: str
