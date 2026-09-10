from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import json
import os

from app.core.config import settings
from app.api.router import api_router

from app.engines.data_generator import generate_microgrid_dataset
from app.engines.quality_engine import quality_engine
from app.engines.disaggregation_engine import disaggregation_engine
from app.engines.cause_engine import cause_engine
from app.engines.recommendation_engine import recommendation_manager
from app.engines.verification_engine import verification_engine
from app.core.loader import EQUIPMENT_REGISTRY

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Enable CORS for React frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Programmatic Single Source of Truth for Registered Engines & Services
REGISTERED_ENGINES = {
    "data_generator": "Active (90-day 15-min telemetry)",
    "quality_engine": "Active (Freshness & edge failure simulator)",
    "disaggregation_engine": "Active (Scenario disaggregation)",
    "cause_engine": "Active (Actionable root-cause detection)",
    "recommendation_manager": "Active (Stateful recommendation tracker)",
    "verification_engine": "Active (Baseline vs. Measured experiment)",
    "equipment_registry": f"Active ({len(EQUIPMENT_REGISTRY)} registered loads)",
    "telemetry_router": "Active (/api/data)",
    "disaggregation_router": "Active (/api/disaggregation)",
    "recommendations_router": "Active (/api/recommendations)",
    "verification_router": "Active (/api/verification)",
    "equipment_router": "Active (/api/equipment)",
    "quality_router": "Active (/api/quality)",
    "i18n_translator": "Active (English & Hindi support)",
    "cors_middleware": "Active (Allow all origins)",
    "baseline_regression_model": "Active (IPMVP compliant historical model)",
    "edge_failure_simulator": "Active (Missing, Stale, Stuck sensor)",
    "drilldown_evidence_engine": "Active (Load-level time series alignment)",
    "role_permission_evaluator": "Active (4 Roles: Operations, Manager, Technician, Resident)"
}

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/api/health")
def health_check():
    """
    Health endpoint reporting programmatically calculated registered service count.
    """
    return {
        "status": "HEALTHY",
        "service_count": len(REGISTERED_ENGINES),
        "services": REGISTERED_ENGINES,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/i18n/{lang}")
def get_i18n_translations(lang: str):
    lang_code = lang.lower()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "i18n", f"{lang_code}.json")
    if not os.path.exists(file_path):
        file_path = os.path.join(base_dir, "i18n", "en.json")
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
