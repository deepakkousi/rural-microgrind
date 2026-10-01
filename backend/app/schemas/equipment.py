from pydantic import BaseModel, Field

class EquipmentItem(BaseModel):
    equipment_id: str = Field(..., description="Unique equipment identifier (e.g. EQ_WP_01)")
    equipment_name: str = Field(..., description="Human-readable equipment name")
    load_tier: str = Field(..., description="Load tier classification (Critical, Essential, Flexible)")
    rated_power_kw: float = Field(..., description="Nameplate power rating in kW")
    location: str = Field(..., description="Physical location on microgrid campus")
    schedule_description: str = Field(..., description="Expected operational operating hours")
    is_essential: bool = Field(..., description="True if load cannot be deferred/shed")
    channel_key: str = Field(..., description="Corresponding telemetry column name")
