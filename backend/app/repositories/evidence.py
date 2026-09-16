from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.evidence import EvidenceItem
from app.models.attribution import AttributionResult, CandidateVesselMatch
from app.models.drift import DriftSimulation
from app.models.report import DataSource, ForensicReport


class EvidenceRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_investigation(self, investigation_id: str) -> List[EvidenceItem]:
        return (
            self.db.query(EvidenceItem)
            .filter(EvidenceItem.investigation_id == investigation_id)
            .all()
        )

    def get_all(self, skip: int = 0, limit: int = 200) -> List[EvidenceItem]:
        return self.db.query(EvidenceItem).offset(skip).limit(limit).all()

    def count(self) -> int:
        return self.db.query(EvidenceItem).count()


class AttributionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_investigation(self, investigation_id: str) -> Optional[AttributionResult]:
        return (
            self.db.query(AttributionResult)
            .filter(AttributionResult.investigation_id == investigation_id)
            .order_by(AttributionResult.created_at.desc())
            .first()
        )

    def create(self, result: AttributionResult) -> AttributionResult:
        self.db.add(result)
        self.db.commit()
        self.db.refresh(result)
        return result


class DriftRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_investigation(self, investigation_id: str) -> Optional[DriftSimulation]:
        return (
            self.db.query(DriftSimulation)
            .filter(DriftSimulation.investigation_id == investigation_id)
            .order_by(DriftSimulation.created_at.desc())
            .first()
        )

    def get_by_id(self, drift_id: str) -> Optional[DriftSimulation]:
        return self.db.query(DriftSimulation).filter(DriftSimulation.id == drift_id).first()

    def create(self, sim: DriftSimulation) -> DriftSimulation:
        self.db.add(sim)
        self.db.commit()
        self.db.refresh(sim)
        return sim


class DataSourceRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[DataSource]:
        return self.db.query(DataSource).all()


class ReportRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_investigation(self, investigation_id: str) -> Optional[ForensicReport]:
        return (
            self.db.query(ForensicReport)
            .filter(ForensicReport.investigation_id == investigation_id)
            .order_by(ForensicReport.generated_at.desc())
            .first()
        )

    def create(self, report: ForensicReport) -> ForensicReport:
        self.db.add(report)
        self.db.commit()
        self.db.refresh(report)
        return report
