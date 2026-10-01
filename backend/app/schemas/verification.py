from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List

class ErrorAnalysisDetail(BaseModel):
    target_reduction_kwh_day: float
    verified_reduction_kwh_day: float
    absolute_error_kwh: float
    percentage_error: float
    sensor_uncertainty: str
    lower_bound_kwh: float
    upper_bound_kwh: float

class InterventionItem(BaseModel):
    id: str
    name: str
    target_equipment: str
    type: str # COST_REDUCTION or ENERGY_REDUCTION
    action: str
    baseline_kwh_day: float
    verification_kwh_day: float
    energy_saving_kwh_day: float
    cost_saving_daily_inr: float
    explanation: str
    status: str

class ReconciliationDetail(BaseModel):
    main_meter_reduction_kwh_day: float
    main_meter_reduction_pct: float
    sum_submeter_reductions_kwh_day: float
    background_unmetered_variance_kwh_day: float
    main_meter_daily_cost_saving_inr: float
    sum_submeter_daily_cost_savings_inr: float
    background_cost_variance_inr: float
    explanation: str

class VerificationSummary(BaseModel):
    status: str = Field("AVAILABLE", description="AVAILABLE or DATA_UNAVAILABLE")
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
    error_analysis: Optional[ErrorAnalysisDetail] = None
    interventions_applied: Optional[List[InterventionItem]] = None
    reconciliation: Optional[ReconciliationDetail] = None

class VerificationTimeseriesPoint(BaseModel):
    day: int
    phase: str
    total_kwh: float
    hvac_kwh: float
    water_pump_kwh: float
    lighting_kwh: float
    avg_occupancy: float
