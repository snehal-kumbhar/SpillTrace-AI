from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel


class CandidateVesselMatchOut(BaseModel):
    id: str
    vessel_id: str
    rank: float
    overall_score: float
    confidence_level: str
    temporal_compatibility: float
    spatial_proximity: float
    drift_consistency: float
    trajectory_compatibility: float
    behaviour_anomaly: float
    counterfactual_similarity: float
    evidence_bullets: List[str] = []
    evidence_strength: str
    counterfactual_spatial_overlap_pct: Optional[float] = None
    counterfactual_centroid_error_km: Optional[float] = None
    counterfactual_shape_similarity: Optional[float] = None
    counterfactual_temporal_consistency: Optional[float] = None
    counterfactual_overall_similarity: Optional[float] = None
    is_simulated: bool

    # Nested vessel info for list views
    vessel_name: Optional[str] = None
    vessel_imo: Optional[str] = None
    vessel_type: Optional[str] = None
    vessel_flag: Optional[str] = None

    class Config:
        from_attributes = True


class AttributionResultOut(BaseModel):
    id: str
    investigation_id: str
    model_version: str
    created_at: datetime
    candidates: List[CandidateVesselMatchOut] = []

    class Config:
        from_attributes = True


class AttributionAnalyzeRequest(BaseModel):
    investigation_id: str
