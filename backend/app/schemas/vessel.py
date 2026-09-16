from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel


class TrajectoryPointOut(BaseModel):
    id: str
    vessel_id: str
    timestamp: datetime
    latitude: float
    longitude: float
    sog_knots: float
    cog_degrees: float
    heading_degrees: Optional[float] = None
    nav_status: str
    is_interpolated: bool

    class Config:
        from_attributes = True


class VesselBase(BaseModel):
    name: str
    imo: str
    mmsi: str
    call_sign: Optional[str] = None
    flag: str
    vessel_type: str
    length_m: float = 245.0
    beam_m: float = 42.0
    draught_m: float = 14.8
    deadweight_tonnage: float = 115000.0
    destination: Optional[str] = None
    current_lat: float
    current_lon: float
    current_sog_knots: float = 12.5
    current_cog_degrees: float = 118.0
    current_heading: float = 119.0
    nav_status: str = "Under way using engine"


class VesselCreate(VesselBase):
    eta: Optional[datetime] = None


class VesselOut(VesselBase):
    id: str
    last_ais_time: datetime
    eta: Optional[datetime] = None
    is_simulated: bool

    class Config:
        from_attributes = True


class VesselWithTrajectoryOut(VesselOut):
    trajectories: List[TrajectoryPointOut] = []


class VesselListOut(BaseModel):
    items: List[VesselOut]
    total: int
