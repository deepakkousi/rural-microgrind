from fastapi import APIRouter
from app.api.routes_data import router as data_router
from app.api.routes_disaggregation import router as disaggregation_router
from app.api.routes_recommendations import router as rec_router
from app.api.routes_verification import router as verification_router
from app.api.routes_equipment import router as equipment_router
from app.api.routes_quality import router as quality_router

api_router = APIRouter()

api_router.include_router(data_router)
api_router.include_router(disaggregation_router)
api_router.include_router(rec_router)
api_router.include_router(verification_router)
api_router.include_router(equipment_router)
api_router.include_router(quality_router)
