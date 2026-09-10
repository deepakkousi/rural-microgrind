from fastapi import APIRouter, HTTPException, Body
from app.engines.recommendation_engine import recommendation_manager
from app.api.routes_data import get_current_df

router = APIRouter(prefix="/recommendations", tags=["Recommendations & Cause Analysis"])

@router.get("")
def get_recommendations():
    df = get_current_df()
    return recommendation_manager.get_all_recommendations(df)

@router.post("/{recommendation_id}/status")
def update_recommendation_status(
    recommendation_id: str,
    payload: dict = Body(...)
):
    status = payload.get("status")
    if not status:
        raise HTTPException(status_code=400, detail="Status field is required.")
    try:
        recommendation_manager.update_recommendation_status(recommendation_id, status)
        return {"recommendation_id": recommendation_id, "status": status, "success": True}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
