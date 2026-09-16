from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Text, Boolean, JSON
from sqlalchemy.orm import relationship
from app.models.base import Base, generate_uuid


class ForensicReport(Base):
    """A generated investigation report."""
    __tablename__ = "forensic_reports"

    id = Column(String(64), primary_key=True, default=generate_uuid)
    investigation_id = Column(String(64), ForeignKey("investigations.id"), nullable=False)

    title = Column(String(255), nullable=False)
    report_type = Column(String(64), default="Full Investigation Report")
    status = Column(String(32), default="Draft")  # Draft | Final | Archived

    # Narrative sections stored as JSON dict: {"section_title": "content", ...}
    sections = Column(JSON, nullable=True)

    # Confidence summary
    overall_confidence = Column(Float, default=0.0)
    data_completeness = Column(Float, default=0.0)
    primary_attribution_score = Column(Float, nullable=True)

    generated_by = Column(String(128), default="SpillTrace AI — Mock Report Engine v1.0")
    generated_at = Column(DateTime, default=datetime.utcnow)
    pdf_url = Column(String(512), nullable=True)  # Future: generated PDF

    disclaimer = Column(
        Text,
        default=(
            "SpillTrace AI provides probabilistic analytical assessments and should not be "
            "interpreted as definitive proof of responsibility. This report is produced for "
            "investigative support purposes only."
        )
    )
    is_simulated = Column(Boolean, default=True)

    investigation = relationship("Investigation", back_populates="reports")


class DataSource(Base):
    """External data source status and metadata."""
    __tablename__ = "data_sources"

    id = Column(String(64), primary_key=True, default=generate_uuid)
    name = Column(String(128), nullable=False, unique=True)
    category = Column(String(64), nullable=False)  # Satellite | AIS | Ocean Currents | Wind | Model
    provider = Column(String(128), nullable=True)
    description = Column(Text, nullable=True)

    status = Column(String(32), default="Online")  # Online | Degraded | Offline
    last_update = Column(DateTime, default=datetime.utcnow)
    update_interval_minutes = Column(Float, default=60.0)
    latency_seconds = Column(Float, nullable=True)
    coverage = Column(String(128), nullable=True)  # e.g. "Global | Indian Ocean"
    records_processed = Column(Float, default=0.0)

    api_endpoint = Column(String(512), nullable=True)
    is_mock = Column(Boolean, default=True)
