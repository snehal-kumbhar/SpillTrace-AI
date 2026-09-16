from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class TimestampMixin(BaseModel):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class GeoPoint(BaseModel):
    lat: float
    lon: float


class HealthResponse(BaseModel):
    status: str
    version: str
    environment: str
    is_mock: bool
    timestamp: datetime
