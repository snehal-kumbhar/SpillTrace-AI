"""Mock report generator. Replace with PDF generation service."""
from datetime import datetime
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session

from app.models.report import ForensicReport
from app.repositories.investigations import InvestigationRepository
from app.repositories.evidence import AttributionRepository, ReportRepository


DISCLAIMER = (
    "SpillTrace AI provides probabilistic analytical assessments and should not be "
    "interpreted as definitive proof of responsibility. This report is produced for "
    "investigative support purposes only."
)


class MockReportGenerator:

    def generate(self, db: Session, investigation_id: str) -> ForensicReport:
        inv_repo = InvestigationRepository(db)
        attr_repo = AttributionRepository(db)
        report_repo = ReportRepository(db)

        inv = inv_repo.get_by_id(investigation_id)
        if not inv:
            raise ValueError(f"Investigation {investigation_id} not found")

        attr = attr_repo.get_by_investigation(investigation_id)
        primary_score = None
        candidate_summary = "No candidate vessels identified."
        if attr and attr.candidates:
            top = attr.candidates[0]
            primary_score = top.overall_score
            candidate_summary = (
                f"Highest-ranked candidate: {top.vessel.name if top.vessel else top.vessel_id} "
                f"— Overall Score: {top.overall_score}/100 ({top.confidence_level})."
            )

        sections = {
            "1. Incident Summary": (
                f"Investigation {inv.reference_code}: {inv.title}. "
                f"Detected at {inv.center_lat}°N, {inv.center_lon}°E. "
                f"Estimated area: {inv.estimated_area_km2} km². "
                f"Detection confidence: {inv.detection_confidence}%."
            ),
            "2. Spill Detection": (
                f"Satellite source: {inv.satellite_source}. "
                f"Estimated spill age: {inv.estimated_spill_age_hours}. "
                f"Detection performed using mock SAR segmentation model."
            ),
            "3. Estimated Origin": (
                "Backward drift reconstruction performed using mock Lagrangian simulation. "
                "See drift analysis module for probability zones and uncertainty bounds."
            ),
            "4. Environmental Conditions": (
                "Wind and ocean current data sourced from ERA5 and CMEMS reanalysis (simulated). "
                "Environmental inputs used for drift modelling are flagged as demo data."
            ),
            "5. AIS Correlation": (
                "Historical AIS trajectories correlated with estimated origin zone and time window. "
                "All vessel data is simulated for demonstration purposes."
            ),
            "6. Candidate Vessels": candidate_summary,
            "7. Attribution Analysis": (
                "Multi-evidence attribution scoring applied. "
                "Scores reflect probabilistic likelihood, not definitive causation."
            ),
            "8. Counterfactual Simulation": (
                "Forward drift simulations performed for top candidate vessels. "
                "Spatial overlap and shape similarity metrics computed (mock)."
            ),
            "9. Evidence": (
                "Evidence items collected from SAR, AIS, drift, environmental, and behavioural sources. "
                "All evidence flagged as simulated demo data."
            ),
            "10. Confidence & Limitations": (
                f"Overall investigation confidence: {primary_score or inv.detection_confidence}%. "
                "Limitations: mock data only; drift model uses reanalysis not real-time feeds; "
                "AIS coverage gaps possible; oil type identification based on SAR characteristics only."
            ),
        }

        report = ForensicReport(
            investigation_id=investigation_id,
            title=f"SpillTrace AI Investigation Report — {inv.reference_code}",
            report_type="Full Investigation Report",
            status="Draft",
            sections=sections,
            overall_confidence=primary_score or inv.detection_confidence,
            data_completeness=round(random_completeness(), 1),
            primary_attribution_score=primary_score,
            generated_by="SpillTrace AI — Mock Report Engine v1.0",
            generated_at=datetime.utcnow(),
            disclaimer=DISCLAIMER,
            is_simulated=True,
        )
        return report_repo.create(report)


def random_completeness() -> float:
    import random
    return random.uniform(82.0, 96.0)
