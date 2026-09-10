import os
from pydantic import BaseModel
from typing import List, Dict

class Settings(BaseModel):
    PROJECT_NAME: str = "Rural Microgrid Intelligence Platform"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    
    # Dataset Parameters
    DATA_DAYS: int = 90
    INTERVAL_MINUTES: int = 15
    RECORDS_PER_DAY: int = 96
    TOTAL_RECORDS: int = 90 * 96 # 8,640 records
    
    # Data Quality & Freshness Thresholds
    LIVE_THRESHOLD_MINUTES: float = 15.0
    STALE_THRESHOLD_MINUTES: float = 120.0 # 2 hours
    
    # Unified Tariff Source of Truth (in ₹ / kWh)
    TARIFF_RATES: Dict[str, float] = {
        "OFF_PEAK": 4.5,
        "SHOULDER": 7.0,
        "PEAK": 12.0
    }
    
    # Default currency
    CURRENCY_SYMBOL: str = "₹"
    CURRENCY_CODE: str = "INR"

    # Configurable CORS Origins
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000"
    ]

settings = Settings()
