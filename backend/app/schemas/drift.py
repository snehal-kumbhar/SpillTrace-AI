from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel


class DriftSimulateRequest(BaseModel):
    investigation_id: str
    particle_count: int = 500
    total_hours: float = 8.0


class ProbabilityZones(BaseModel):
    high: List[List[float]]    # [[lon, lat], ...]
    medium: List[List[float]]
    low: List[List[float]]


class ParticleTrackPoint(BaseModel):
    lat: float
    lon: float
    timestamp: str
    probability: float


class DriftSimulationOut(BaseModel):
    id: str
    investigation_id: str
    simulation_type: str
    model_version: str
    particle_count: int
    time_step_hours: float
    total_hours: float
    origin_lat: float
    origin_lon: float
    origin_uncertainty_km: float
    origin_probability: float
    origin_time_start: Optional[datetime] = None
    origin_time_end: Optional[datetime] = None
    probability_zones: Optional[Any] = None
    particle_tracks: Optional[Any] = None
    current_dataset: str
    wind_dataset: str
    wind_speed_ms: float
    wind_direction_deg: float
    current_speed_ms: float
    current_direction_deg: float
    is_simulated: bool
    created_at: datetime

    class Config:
        from_attributes = True
