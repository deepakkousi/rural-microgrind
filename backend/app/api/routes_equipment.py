from fastapi import APIRouter, HTTPException
from app.core.loader import get_all_equipment, get_equipment_by_id

router = APIRouter(prefix="/equipment", tags=["Equipment Registry"])

@router.get("")
def get_equipment_registry():
    return get_all_equipment()

@router.get("/{equipment_id}")
def get_single_equipment(equipment_id: str):
    try:
        return get_equipment_by_id(equipment_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
