from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel


class InvestigationBase(BaseModel):
    reference_code: str
    title: str
    status: str = "Under Investigation"
    priority: str = "High"
    region: str
    estimated_area_km2: float = 0.0
    detection_confidence: float = 0.0
    estimated_spill_age_hours: str = "4-6 hours"
    satellite_source: str = "Sentinel-1A SAR C-Band"
    center_lat: float
    center_lon: float
    summary: Optional[str] = None
    current_stage: int = 1


class InvestigationCreate(InvestigationBase):
    detection_time: Optional[datetime] = None


class InvestigationUpdate(BaseModel):
    title: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    current_stage: Optional[int] = None
    summary: Optional[str] = None


class InvestigationOut(InvestigationBase):
    id: str
    detection_time: datetime
    created_at: datetime
    updated_at: datetime
    disclaimer: Optional[str] = None

    class Config:
        from_attributes = True


class InvestigationListOut(BaseModel):
    items: List[InvestigationOut]
    total: int
