from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List

class TierValue(BaseModel):
    kw: float
    pct: float

class DisaggregationTiers(BaseModel):
    critical: TierValue
    essential: TierValue
    flexible: TierValue

class DetailedLoadItem(BaseModel):
    equipment_id: str
    equipment_name: str
    load_tier: str
    rated_power_kw: float
    current_power_kw: float
    percentage: float
    location: str
    is_essential: bool
    schedule: str

class DisaggregationEvaluation(BaseModel):
    mae_kw: float
    rmse_kw: float
    mape_pct: float
    wape_pct: float

class DisaggregationSummary(BaseModel):
    timestamp: str
    total_kw: float
    tiers: DisaggregationTiers
    evaluation_metrics: DisaggregationEvaluation
    detailed_loads: List[DetailedLoadItem]
    components: Optional[Dict[str, float]] = None
    percentage_breakdown: Optional[Dict[str, float]] = None

class DrilldownPoint(BaseModel):
    timestamp: str
    actual_kw: float
    expected_kw: float
    occupancy_pct: float
    tariff_rate: float
    tariff_period: str

class DrilldownResponse(BaseModel):
    equipment_id: str
    equipment_name: str
    load_tier: str
    impact_type: str
    location: str
    rated_power_kw: float
    is_essential: bool
    schedule: str
    cause_explanation: str
    recommended_action: str
    timeseries: List[DrilldownPoint]
