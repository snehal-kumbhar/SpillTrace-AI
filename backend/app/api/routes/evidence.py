from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.repositories.evidence import EvidenceRepository
from app.schemas.evidence import EvidenceListOut

router = APIRouter(prefix="/evidence", tags=["Evidence"])


@router.get("", response_model=EvidenceListOut)
def list_evidence(
    investigation_id: Optional[str] = None,
    skip: int = 0,
    limit: int = 200,
    db: Session = Depends(get_db),
):
    repo = EvidenceRepository(db)
    if investigation_id:
        items = repo.get_by_investigation(investigation_id)
    else:
        items = repo.get_all(skip=skip, limit=limit)
    return EvidenceListOut(items=items, total=len(items) if investigation_id else repo.count())
