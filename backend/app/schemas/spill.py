from typing import Optional, List, Any
from datetime import datetime
from pydantic import BaseModel


class SpillDetectionOut(BaseModel):
    id: str
    spill_id: str
    satellite_name: str
    sensor_type: str
    acquisition_time: datetime
    confidence: float
    mean_backscatter_db: float
    ambient_backscatter_db: float
    contrast_db: float
    incidence_angle_deg: float
    polarization: str
    biogenic_slick_rejection: float
    low_wind_calm_rejection: float
    internal_wave_rejection: float
    rain_cell_rejection: float
    sar_preview_url: Optional[str] = None
    mask_geometry: Optional[Any] = None

    class Config:
        from_attributes = True


class SpillEventBase(BaseModel):
    name: str
    center_lat: float
    center_lon: float
    polygon_coordinates: List[List[float]]
    area_km2: float
    estimated_volume_m3: float = 125.0
    oil_type: str = "Heavy Crude Oil (API 28.5)"
    estimated_age_min_hours: float = 4.0
    estimated_age_max_hours: float = 6.5


class SpillEventCreate(SpillEventBase):
    investigation_id: str
    detected_at: Optional[datetime] = None


class SpillEventOut(SpillEventBase):
    id: str
    investigation_id: str
    detected_at: datetime
    detections: List[SpillDetectionOut] = []

    class Config:
        from_attributes = True


class SpillListOut(BaseModel):
    items: List[SpillEventOut]
    total: int


class DetectRequest(BaseModel):
    """Request to run spill detection on a (mock) SAR image."""
    investigation_id: str
    image_url: Optional[str] = None
    region: Optional[str] = None
