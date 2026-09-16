from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.repositories.investigations import InvestigationRepository
from app.repositories.spills import SpillRepository
from app.repositories.evidence import DriftRepository, AttributionRepository, EvidenceRepository, ReportRepository
from app.schemas.investigation import InvestigationOut, InvestigationListOut, InvestigationCreate
from app.schemas.spill import SpillEventOut
from app.schemas.drift import DriftSimulationOut
from app.schemas.attribution import AttributionResultOut, CandidateVesselMatchOut
from app.schemas.evidence import EvidenceListOut
from app.schemas.report import ForensicReportOut

router = APIRouter(prefix="/investigations", tags=["Investigations"])


def _enrich_candidate(c) -> CandidateVesselMatchOut:
    out = CandidateVesselMatchOut.model_validate(c)
    if c.vessel:
        out.vessel_name = c.vessel.name
        out.vessel_imo = c.vessel.imo
        out.vessel_type = c.vessel.vessel_type
        out.vessel_flag = c.vessel.flag
    return out


@router.get("", response_model=InvestigationListOut)
def list_investigations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    repo = InvestigationRepository(db)
    items = repo.get_all(skip=skip, limit=limit)
    return InvestigationListOut(items=items, total=repo.count())


@router.get("/{investigation_id}", response_model=InvestigationOut)
def get_investigation(investigation_id: str, db: Session = Depends(get_db)):
    repo = InvestigationRepository(db)
    inv = repo.get_by_id(investigation_id)
    if not inv:
        raise HTTPException(status_code=404, detail="Investigation not found")
    return inv


@router.post("", response_model=InvestigationOut, status_code=201)
def create_investigation(payload: InvestigationCreate, db: Session = Depends(get_db)):
    from app.models.investigation import Investigation
    repo = InvestigationRepository(db)
    inv = Investigation(**payload.model_dump())
    return repo.create(inv)


@router.get("/{investigation_id}/spills", response_model=List[SpillEventOut])
def get_investigation_spills(investigation_id: str, db: Session = Depends(get_db)):
    repo = SpillRepository(db)
    return repo.get_by_investigation(investigation_id)


@router.get("/{investigation_id}/drift", response_model=DriftSimulationOut)
def get_investigation_drift(investigation_id: str, db: Session = Depends(get_db)):
    repo = DriftRepository(db)
    sim = repo.get_by_investigation(investigation_id)
    if not sim:
        raise HTTPException(status_code=404, detail="Drift simulation not found")
    return sim


@router.get("/{investigation_id}/attribution", response_model=AttributionResultOut)
def get_investigation_attribution(investigation_id: str, db: Session = Depends(get_db)):
    repo = AttributionRepository(db)
    result = repo.get_by_investigation(investigation_id)
    if not result:
        raise HTTPException(status_code=404, detail="Attribution result not found")
    out = AttributionResultOut.model_validate(result)
    out.candidates = [_enrich_candidate(c) for c in result.candidates]
    return out


@router.get("/{investigation_id}/evidence", response_model=EvidenceListOut)
def get_investigation_evidence(investigation_id: str, db: Session = Depends(get_db)):
    repo = EvidenceRepository(db)
    items = repo.get_by_investigation(investigation_id)
    return EvidenceListOut(items=items, total=len(items))


@router.get("/{investigation_id}/report", response_model=ForensicReportOut)
def get_investigation_report(investigation_id: str, db: Session = Depends(get_db)):
    repo = ReportRepository(db)
    report = repo.get_by_investigation(investigation_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report
