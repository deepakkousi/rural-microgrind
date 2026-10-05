from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List

class CauseEvidence(BaseModel):
    metric: str
    observed_value: float
    expected_value: float
    context: str

class Recommendation(BaseModel):
    recommendation_id: str = Field(..., description="Unique recommendation identifier")
    equipment_id: str = Field(..., description="Target equipment identifier")
    equipment_name: str = Field(..., description="Target equipment name")
    load_tier: str = Field(..., description="Classification tier (Critical, Essential, Flexible)")
    action_type: str = Field("COST_REDUCTION", description="COST_REDUCTION (LOAD SHIFT) or ENERGY_REDUCTION")
    problem: str = Field(..., description="Plain-language description of detected inefficiency")
    cause: str = Field(..., description="Underlying root-cause explanation")
    evidence: CauseEvidence = Field(..., description="Quantified evidence signals")
    recommended_action: str = Field(..., description="Operational action recommended to microgrid operator")
    daily_energy_saving_kwh: float = Field(0.0, description="Daily energy reduction in kWh (0.0 for pure load shifts)")
    daily_cost_saving: float = Field(0.0, description="Daily financial cost saving in INR")
    estimated_energy_saving_kwh: float = Field(0.0, description="Monthly energy reduction in kWh (daily_energy_saving_kwh * 30)")
    estimated_cost_saving: float = Field(..., description="Estimated monthly financial cost saving in INR (daily_cost_saving * 30)")
    evidence_score: int = Field(90, description="Transparent 0-100 heuristic evidence strength score")
    evidence_breakdown: Dict[str, int] = Field(default_factory=dict, description="Point contribution breakdown")
    evidence_strength_normalized: Optional[float] = Field(None, description="Normalized representation of heuristic Evidence Strength Score (evidence_score / 100.0, 0.0 - 1.0); NOT statistical confidence")
    confidence: float = Field(..., description="Normalized representation of the heuristic Evidence Strength Score (evidence_score / 100.0) retained for backward compatibility; NOT statistical confidence.")
    data_freshness: str = Field(..., description="Freshness status (LIVE, STALE, VERY_STALE, MISSING)")
    priority: str = Field(..., description="Priority level (HIGH, MEDIUM, LOW)")
    status: str = Field("PENDING", description="Stateful status (PENDING, APPLIED, REJECTED)")

class StatusUpdateRequest(BaseModel):
    status: str = Field(..., description="New status to apply (PENDING, APPLIED, REJECTED)")

class StatusUpdateResponse(BaseModel):
    recommendation_id: str
    status: str
    success: bool
