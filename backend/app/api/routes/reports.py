from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.repositories.evidence import ReportRepository
from app.schemas.report import ForensicReportOut, ForensicReportGenerateRequest
from app.services.factory import get_report_generator

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.post("", response_model=ForensicReportOut, status_code=201)
def generate_report(payload: ForensicReportGenerateRequest, db: Session = Depends(get_db)):
    generator = get_report_generator()
    try:
        report = generator.generate(db, payload.investigation_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return report


@router.get("/investigations/{investigation_id}", response_model=ForensicReportOut)
def get_investigation_report(investigation_id: str, db: Session = Depends(get_db)):
    repo = ReportRepository(db)
    report = repo.get_by_investigation(investigation_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report
