from fastapi import APIRouter, HTTPException
from app.engines.disaggregation_engine import disaggregation_engine
from app.api.routes_data import get_current_df

router = APIRouter(prefix="/disaggregation", tags=["Load Disaggregation"])

@router.get("")
def get_load_disaggregation():
    df = get_current_df()
    return disaggregation_engine.disaggregate_dataframe(df)

@router.get("/drilldown/{load_id}")
def get_drilldown_evidence(load_id: str):
    df = get_current_df()
    try:
        return disaggregation_engine.get_drilldown_evidence(df, load_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
