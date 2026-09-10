import os
from pydantic import BaseModel

class Settings(BaseModel):
    PROJECT_NAME: str = "Rural Microgrid Intelligence Platform"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    
    # Dataset Parameters
    DATA_DAYS: int = 90
    INTERVAL_MINUTES: int = 15
    RECORDS_PER_DAY: int = 96
    TOTAL_RECORDS: int = 90 * 96 # 8640
    
    # Failure thresholds
    LIVE_THRESHOLD_MINUTES: float = 15.0
    STALE_THRESHOLD_MINUTES: float = 120.0 # 2 hours
    
    # Default currency
    CURRENCY_SYMBOL: str = "₹"
    CURRENCY_CODE: str = "INR"

settings = Settings()
