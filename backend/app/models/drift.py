from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime, Integer, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from app.models.base import Base, generate_uuid


class DriftSimulation(Base):
    """Lagrangian backward-drift simulation result for an investigation."""
    __tablename__ = "drift_simulations"

    id = Column(String(64), primary_key=True, default=generate_uuid)
    investigation_id = Column(String(64), ForeignKey("investigations.id"), nullable=False)

    # Simulation configuration
    simulation_type = Column(String(32), default="backward")  # backward | forward
    model_version = Column(String(32), default="mock-v1.0")
    particle_count = Column(Integer, default=500)
    time_step_hours = Column(Float, default=1.0)
    total_hours = Column(Float, default=8.0)  # hours simulated back in time

    # Origin estimate (high-probability centroid)
    origin_lat = Column(Float, nullable=False)
    origin_lon = Column(Float, nullable=False)
    origin_uncertainty_km = Column(Float, default=7.4)
    origin_probability = Column(Float, default=0.78)  # 0–1

    # Time window for probable spill event
    origin_time_start = Column(DateTime, nullable=True)
    origin_time_end = Column(DateTime, nullable=True)

    # Probability zones stored as GeoJSON-compatible polygons
    # {"high": [[lon,lat],...], "medium": [[lon,lat],...], "low": [[lon,lat],...]}
    probability_zones = Column(JSON, nullable=True)

    # Particle track paths: list of [{lat, lon, timestamp, probability}]
    particle_tracks = Column(JSON, nullable=True)

    # Environmental inputs used
    current_dataset = Column(String(128), default="CMEMS GLORYS12 (simulated)")
    wind_dataset = Column(String(128), default="ERA5 Reanalysis (simulated)")
    wind_speed_ms = Column(Float, default=8.2)
    wind_direction_deg = Column(Float, default=245.0)
    current_speed_ms = Column(Float, default=0.45)
    current_direction_deg = Column(Float, default=310.0)

    is_simulated = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    investigation = relationship("Investigation", back_populates="drift_simulations")
