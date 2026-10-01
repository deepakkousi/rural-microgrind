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

# Configurable CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    code_map = {
        400: "INVALID_REQUEST",
        401: "UNAUTHORIZED",
        403: "FORBIDDEN",
        404: "RESOURCE_NOT_FOUND",
        405: "METHOD_NOT_ALLOWED",
        422: "VALIDATION_ERROR",
        500: "INTERNAL_SERVER_ERROR"
    }
    code = code_map.get(exc.status_code, f"HTTP_{exc.status_code}")
    message = str(exc.detail) if isinstance(exc.detail, str) else "HTTP Request Error"
    details = exc.detail if isinstance(exc.detail, (dict, list)) else {}
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": code,
                "message": message,
                "details": details,
                "timestamp": datetime.now().isoformat()
            },
            "detail": exc.detail
        }
    )

@app.exception_handler(RequestValidationError)
async def custom_validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Invalid request parameters or payload structure.",
                "details": {"validation_errors": exc.errors()},
                "timestamp": datetime.now().isoformat()
            },
            "detail": exc.errors()
        }
    )

# Core Calculation Engines
CORE_ENGINES = {
    "data_generator": "Active (90-day 15-min telemetry)",
    "quality_engine": "Active (Freshness & edge failure simulator)",
    "disaggregation_engine": "Active (Scenario disaggregation)",
    "cause_engine": "Active (Actionable root-cause detection)",
    "recommendation_manager": "Active (Stateful recommendation tracker)",
    "verification_engine": "Active (Historical baseline vs. Measured experiment)"
}

# Total Registered API Services & Routes
REGISTERED_SERVICES = {
    **CORE_ENGINES,
    "equipment_registry": f"Active ({len(EQUIPMENT_REGISTRY)} registered loads)",
    "telemetry_router": "Active (/api/data)",
    "disaggregation_router": "Active (/api/disaggregation)",
    "recommendations_router": "Active (/api/recommendations)",
    "verification_router": "Active (/api/verification)",
    "equipment_router": "Active (/api/equipment)",
    "quality_router": "Active (/api/quality)",
    "i18n_translator": "Active (English & Hindi support)",
    "cors_middleware": "Active (Configured CORS origins)",
    "baseline_model": "Active (Historical baseline model)",
    "edge_failure_simulator": "Active (Missing, Stale, Stuck sensor)",
    "drilldown_evidence_engine": "Active (Load-level time series alignment)",
    "role_permission_evaluator": "Active (4 Roles: Operations, Manager, Technician, Resident)"
}

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/api/health")
def health_check():
    """
    Health endpoint returning engine count and registered components.
    """
    return {
        "status": "HEALTHY",
        "engine_count": len(CORE_ENGINES),
        "service_count": len(REGISTERED_SERVICES),
        "engines": CORE_ENGINES,
        "services": REGISTERED_SERVICES,
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

@app.get("/api/v1/openapi.json", include_in_schema=False)
def get_openapi_v1_alias():
    return app.openapi()

@app.get("/api/user/roles")
@app.get("/api/user/role")
def get_user_roles():
    return {
        "roles": [
            {"id": "operations", "name": "Operations Staff", "description": "Active alerts and operational recommendations"},
            {"id": "manager", "name": "Microgrid Manager", "description": "Financial metrics and verified savings"},
            {"id": "technician", "name": "Technician", "description": "Sensor health and failure simulation"},
            {"id": "resident", "name": "Resident / Non-Technical User", "description": "Plain-language disaggregation summary"}
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
