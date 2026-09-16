from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from app.models.base import Base, generate_uuid


class EvidenceItem(Base):
    """A piece of forensic evidence associated with an investigation."""
    __tablename__ = "evidence_items"

    id = Column(String(64), primary_key=True, default=generate_uuid)
    investigation_id = Column(String(64), ForeignKey("investigations.id"), nullable=False)

    # Classification
    evidence_type = Column(String(64), nullable=False)
    # Types: SAR Imagery | AIS Trajectory | Wind Data | Ocean Current Data |
    #        Drift Simulation | Vessel Behaviour | Counterfactual Simulation | Model Prediction

    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    source = Column(String(128), nullable=False)   # e.g. "Sentinel-1A / ESA Copernicus"
    asset_url = Column(String(512), nullable=True)  # URI to associated file/image

    # Scoring
    confidence = Column(Float, default=0.0)    # 0–100
    relevance = Column(Float, default=0.0)     # 0–100 relevance to case
    weight = Column(Float, default=1.0)        # scoring weight

    # Timing
    evidence_timestamp = Column(DateTime, nullable=True)  # when the evidence was captured
    ingested_at = Column(DateTime, default=datetime.utcnow)

    is_simulated = Column(Boolean, default=True)

    investigation = relationship("Investigation", back_populates="evidence_items")
