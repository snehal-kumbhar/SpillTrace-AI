from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, JSON, Boolean, Text
from sqlalchemy.orm import relationship
from app.models.base import Base, generate_uuid


class AttributionResult(Base):
    """Master attribution result linking an investigation to ranked candidate vessels."""
    __tablename__ = "attribution_results"

    id = Column(String(64), primary_key=True, default=generate_uuid)
    investigation_id = Column(String(64), ForeignKey("investigations.id"), nullable=False)
    model_version = Column(String(32), default="mock-attribution-v1.0")
    created_at = Column(DateTime, default=datetime.utcnow)

    investigation = relationship("Investigation", back_populates="attributions")
    candidates = relationship("CandidateVesselMatch", back_populates="attribution_result",
                              cascade="all, delete-orphan",
                              order_by="CandidateVesselMatch.rank")


class CandidateVesselMatch(Base):
    """A vessel ranked as a potential source for a spill event."""
    __tablename__ = "candidate_vessel_matches"

    id = Column(String(64), primary_key=True, default=generate_uuid)
    attribution_result_id = Column(String(64), ForeignKey("attribution_results.id"), nullable=False)
    vessel_id = Column(String(64), ForeignKey("vessels.id"), nullable=False)

    rank = Column(Float, nullable=False)  # 1 = highest likelihood
    overall_score = Column(Float, nullable=False)  # 0–100
    confidence_level = Column(String(32), default="Medium")  # High | Medium | Low

    # Sub-scores (0–100 each)
    temporal_compatibility = Column(Float, default=0.0)   # Was vessel in area during spill window?
    spatial_proximity = Column(Float, default=0.0)         # Distance to origin zone
    drift_consistency = Column(Float, default=0.0)         # Trajectory matches drift vector
    trajectory_compatibility = Column(Float, default=0.0)  # Overall path match
    behaviour_anomaly = Column(Float, default=0.0)         # Speed/course anomalies
    counterfactual_similarity = Column(Float, default=0.0) # Counterfactual simulation overlap

    # Explainability evidence (list of text bullets)
    evidence_bullets = Column(JSON, default=list)   # List[str]
    evidence_strength = Column(String(32), default="Moderate")  # Strong | Moderate | Weak

    # Counterfactual simulation metrics
    counterfactual_spatial_overlap_pct = Column(Float, nullable=True)
    counterfactual_centroid_error_km = Column(Float, nullable=True)
    counterfactual_shape_similarity = Column(Float, nullable=True)
    counterfactual_temporal_consistency = Column(Float, nullable=True)
    counterfactual_overall_similarity = Column(Float, nullable=True)

    is_simulated = Column(Boolean, default=True)

    attribution_result = relationship("AttributionResult", back_populates="candidates")
    vessel = relationship("Vessel", back_populates="attribution_matches")
