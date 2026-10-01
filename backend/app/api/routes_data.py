from fastapi import APIRouter, Query, HTTPException
from typing import Optional, Dict, Any, List
from app.engines.data_generator import generate_microgrid_dataset
from app.engines.quality_engine import quality_engine

router = APIRouter(prefix="/data", tags=["Data Telemetry"])

# Global in-memory dataset cache
DATASET_CACHE = generate_microgrid_dataset()

def get_current_df():
    global DATASET_CACHE
    if DATASET_CACHE.empty:
        DATASET_CACHE = generate_microgrid_dataset()
    # Apply simulated quality checks / failures
    return quality_engine.apply_quality_checks_and_failures(DATASET_CACHE)

@router.get("/meter")
def get_meter_telemetry(limit: int = Query(96, ge=1, le=8640)):
    df = get_current_df()
    sliced = df.tail(limit)
    return sliced.to_dict(orient="records")

@router.get("/context")
def get_context_data(limit: int = Query(96, ge=1, le=8640)):
    df = get_current_df()
    sliced = df.tail(limit)[['timestamp', 'occupancy', 'tariff_period', 'tariff_rate', 'solar_gen_kw']]
    return sliced.to_dict(orient="records")

@router.get("/summary")
def get_data_summary():
    df = get_current_df()
    latest = df.iloc[-1].to_dict()
    return {
        "total_records": len(df),
        "latest_record": latest,
        "date_range": {
            "start": df.iloc[0]['timestamp'],
            "end": df.iloc[-1]['timestamp']
        }
    }

@router.get("/tariff")
def get_tariff_structure():
    from app.core.config import settings
    return {
        "currency": settings.CURRENCY_CODE,
        "currency_symbol": settings.CURRENCY_SYMBOL,
        "rates": settings.TARIFF_RATES,
        "periods": [
            {
                "period": "OFF_PEAK",
                "rate": settings.TARIFF_RATES.get("OFF_PEAK", 4.5),
                "hours": "22:00 - 06:00",
                "description": "Late night / early morning off-peak window"
            },
            {
                "period": "SHOULDER",
                "rate": settings.TARIFF_RATES.get("SHOULDER", 7.0),
                "hours": "06:00 - 14:00, 19:00 - 22:00",
                "description": "Daytime standard operation window"
            },
            {
                "period": "PEAK",
                "rate": settings.TARIFF_RATES.get("PEAK", 12.0),
                "hours": "14:00 - 19:00",
                "description": "Afternoon peak demand surcharge window"
            }
        ]
    }
