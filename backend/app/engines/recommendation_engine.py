import pandas as pd
from typing import List, Optional
from app.core.schemas import Recommendation
from app.engines.cause_engine import cause_engine

class RecommendationManager:
    def __init__(self):
        self.applied_status: dict = {}

    def get_all_recommendations(self, df: pd.DataFrame) -> List[Recommendation]:
        recs = cause_engine.analyze_causes_and_recommendations(df)
        
        # Override status if user updated it via API
        for rec in recs:
            if rec.recommendation_id in self.applied_status:
                rec.status = self.applied_status[rec.recommendation_id]
                
        return recs

    def update_recommendation_status(self, rec_id: str, new_status: str) -> bool:
        if new_status not in ["PENDING", "APPLIED", "REJECTED"]:
            raise ValueError(f"Invalid recommendation status: {new_status}")
        self.applied_status[rec_id] = new_status
        return True

recommendation_manager = RecommendationManager()
