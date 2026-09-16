from typing import Optional, Dict, Any, List
from datetime import datetime
from pydantic import BaseModel


class DataSourceOut(BaseModel):
    id: str
    name: str
    category: str
    provider: Optional[str] = None
    description: Optional[str] = None
    status: str
    last_update: datetime
    update_interval_minutes: float
    latency_seconds: Optional[float] = None
    coverage: Optional[str] = None
    records_processed: float
    is_mock: bool

    class Config:
        from_attributes = True


class ForensicReportGenerateRequest(BaseModel):
    investigation_id: str


class ForensicReportOut(BaseModel):
    id: str
    investigation_id: str
    title: str
    report_type: str
    status: str
    sections: Optional[Dict[str, Any]] = None
    overall_confidence: float
    data_completeness: float
    primary_attribution_score: Optional[float] = None
    generated_by: str
    generated_at: datetime
    pdf_url: Optional[str] = None
    disclaimer: str
    is_simulated: bool

    class Config:
        from_attributes = True
