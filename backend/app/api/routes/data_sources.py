from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.repositories.evidence import DataSourceRepository
from app.schemas.report import DataSourceOut

router = APIRouter(prefix="/data-sources", tags=["Data Sources"])


@router.get("", response_model=List[DataSourceOut])
def list_data_sources(db: Session = Depends(get_db)):
    repo = DataSourceRepository(db)
    return repo.get_all()
