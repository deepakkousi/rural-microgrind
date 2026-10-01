from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List

class TelemetryRecord(BaseModel):
    timestamp: str = Field(..., description="ISO-8601 formatted timestamp")
    total_kw: float = Field(..., description="Total microgrid power in kW")
    lighting_kw: float = Field(..., description="Lighting circuit load in kW")
    hvac_kw: float = Field(..., description="HVAC chiller load in kW")
    water_pump_kw: float = Field(..., description="Water pump load in kW")
    lab_equipment_kw: float = Field(..., description="Workshop equipment load in kW")
    kitchen_kw: float = Field(..., description="Kitchen load in kW")
    it_network_kw: float = Field(..., description="IT / Server load in kW")
    solar_gen_kw: float = Field(..., description="Solar PV generation in kW")
    occupancy: float = Field(..., description="Campus occupancy percentage (0-100%)")
    tariff_period: str = Field(..., description="Tariff tier (OFF_PEAK, SHOULDER, PEAK)")
    tariff_rate: float = Field(..., description="Electricity tariff in INR/kWh")
    net_grid_kw: float = Field(..., description="Net grid import/export in kW")
    day_index: Optional[int] = Field(None, description="Day index in experiment (1-90)")

class ContextRecord(BaseModel):
    timestamp: str = Field(..., description="ISO-8601 timestamp")
    occupancy: float = Field(..., description="Campus occupancy percentage")
    tariff_period: str = Field(..., description="Active tariff period")
    tariff_rate: float = Field(..., description="Tariff rate in INR/kWh")
    solar_gen_kw: float = Field(..., description="Solar generation in kW")

class DateRange(BaseModel):
    start: str
    end: str

class TelemetrySummary(BaseModel):
    total_records: int
    latest_record: Dict[str, Any]
    date_range: DateRange
