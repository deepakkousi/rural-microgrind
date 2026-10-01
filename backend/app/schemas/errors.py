from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class ErrorDetail(BaseModel):
    code: str = Field(..., description="Machine-readable error code (e.g. STALE_DATA, INVALID_REQUEST)")
    message: str = Field(..., description="Human-readable explanation of the error")
    details: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional contextual details")
    timestamp: str = Field(..., description="ISO-8601 timestamp when error occurred")

class ErrorResponse(BaseModel):
    error: ErrorDetail
    detail: Optional[Any] = Field(None, description="FastAPI legacy compatibility detail string or object")
