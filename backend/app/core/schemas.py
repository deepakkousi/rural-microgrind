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
    evaluation: Dict[str, float] # MAE, RMSE, MAPE

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
    problem: str
    cause: str
    evidence: CauseEvidence
    recommended_action: str
    estimated_energy_saving_kwh: float
    estimated_cost_saving: float
    confidence: float # 0.0 to 1.0
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
    baseline_period: str
    intervention_period: str
    verification_period: str
    baseline_daily_avg_kwh: float
    target_daily_avg_kwh: float
    measured_daily_avg_kwh: float
    verified_reduction_kwh_day: float
    verified_reduction_pct: float
    cost_saving_daily: float
    cost_saving_total: float
    measurement_error_margin_pct: float
    lower_bound_kwh: float
    upper_bound_kwh: float
    interventions_applied: List[Dict[str, Any]]

class FailureSimulationRequest(BaseModel):
    failure_type: str # MISSING_DATA, STALE_DATA, STUCK_SENSOR, NEGATIVE_READING, TARIFF_REVISION, RESET
    duration_intervals: int = 16 # Default ~4 hours
    affected_channel: Optional[str] = "water_pump_kw"

class HealthResponse(BaseModel):
    status: str
    service_count: int
    services: Dict[str, str]
    timestamp: str
