from fastapi import APIRouter
from app.core.loader import get_all_equipment

router = APIRouter(prefix="/equipment", tags=["Equipment Registry"])

@router.get("")
def get_equipment_registry():
    return get_all_equipment()
