import json
from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime, Text, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base, generate_uuid

class Investigation(Base):
    __tablename__ = "investigations"

    id = Column(String(64), primary_key=True, default=generate_uuid)
    reference_code = Column(String(32), unique=True, nullable=False, index=True) # e.g. INV-2026-0047
    title = Column(String(255), nullable=False)
    status = Column(String(64), default="Under Investigation") # Under Investigation, Attributed - Pending Review, Closed - Inconclusive
    priority = Column(String(32), default="High") # Critical, High, Medium, Low
    region = Column(String(128), nullable=False) # e.g. Arabian Sea, Persian Gulf
    detection_time = Column(DateTime, default=datetime.utcnow)
    
    # Workflow Stage (1-8)
    current_stage = Column(Integer, default=5) # 1: Detection, 2: Characterization, 3: Drift, 4: Origin, 5: AIS Correlation, 6: Vessel Analysis, 7: Attribution, 8: Evidence Review
    
    # Forensic Summary & Metrics
    estimated_area_km2 = Column(Float, default=0.0)
    detection_confidence = Column(Float, default=0.0) # e.g. 94.7
    estimated_spill_age_hours = Column(String(64), default="4-6 hours")
    satellite_source = Column(String(128), default="Sentinel-1A SAR C-Band")
    center_lat = Column(Float, nullable=False)
    center_lon = Column(Float, nullable=False)
    
    summary = Column(Text, nullable=True)
    disclaimer = Column(Text, default="SpillTrace AI provides probabilistic analytical assessments and should not be interpreted as definitive proof of responsibility.")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    spills = relationship("SpillEvent", back_populates="investigation", cascade="all, delete-orphan")
    drift_simulations = relationship("DriftSimulation", back_populates="investigation", cascade="all, delete-orphan")
    attributions = relationship("AttributionResult", back_populates="investigation", cascade="all, delete-orphan")
    evidence_items = relationship("EvidenceItem", back_populates="investigation", cascade="all, delete-orphan")
    reports = relationship("ForensicReport", back_populates="investigation", cascade="all, delete-orphan")
