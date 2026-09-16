from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel


class EvidenceItemOut(BaseModel):
    id: str
    investigation_id: str
    evidence_type: str
    title: str
    description: Optional[str] = None
    source: str
    asset_url: Optional[str] = None
    confidence: float
    relevance: float
    weight: float
    evidence_timestamp: Optional[datetime] = None
    ingested_at: datetime
    is_simulated: bool

    class Config:
        from_attributes = True


class EvidenceListOut(BaseModel):
    items: List[EvidenceItemOut]
    total: int
