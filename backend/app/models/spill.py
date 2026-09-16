from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.models.base import Base, generate_uuid

class SpillEvent(Base):
    __tablename__ = "spill_events"

    id = Column(String(64), primary_key=True, default=generate_uuid)
    investigation_id = Column(String(64), ForeignKey("investigations.id"), nullable=False)
    name = Column(String(255), nullable=False)
    detected_at = Column(DateTime, default=datetime.utcnow)
    
    # Location and Slick Geometry
    center_lat = Column(Float, nullable=False)
    center_lon = Column(Float, nullable=False)
    polygon_coordinates = Column(JSON, nullable=False) # List of [lon, lat] coordinates defining the slick boundary
    
    # Characteristics
    area_km2 = Column(Float, nullable=False)
    estimated_volume_m3 = Column(Float, default=125.0)
    oil_type = Column(String(64), default="Heavy Crude Oil (API 28.5)")
    estimated_age_min_hours = Column(Float, default=4.0)
    estimated_age_max_hours = Column(Float, default=6.5)
    
    # Relationships
    investigation = relationship("Investigation", back_populates="spills")
    detections = relationship("SpillDetection", back_populates="spill", cascade="all, delete-orphan")


class SpillDetection(Base):
    __tablename__ = "spill_detections"

    id = Column(String(64), primary_key=True, default=generate_uuid)
    spill_id = Column(String(64), ForeignKey("spill_events.id"), nullable=False)
    satellite_name = Column(String(64), default="Sentinel-1A")
    sensor_type = Column(String(64), default="C-SAR (IW Mode)")
    acquisition_time = Column(DateTime, default=datetime.utcnow)
    
    # Detection Confidence & Physics Metrics
    confidence = Column(Float, default=94.7)
    mean_backscatter_db = Column(Float, default=-24.6)
    ambient_backscatter_db = Column(Float, default=-14.2)
    contrast_db = Column(Float, default=-10.4)
    incidence_angle_deg = Column(Float, default=36.4)
    polarization = Column(String(16), default="VV+VH")
    
    # Look-Alike Rejection Confidence (0-100)
    biogenic_slick_rejection = Column(Float, default=96.2)
    low_wind_calm_rejection = Column(Float, default=92.8)
    internal_wave_rejection = Column(Float, default=98.5)
    rain_cell_rejection = Column(Float, default=95.1)
    
    # Image Mask Asset URI (or simulated raster data)
    sar_preview_url = Column(String(255), nullable=True)
    mask_geometry = Column(JSON, nullable=True)

    spill = relationship("SpillEvent", back_populates="detections")
