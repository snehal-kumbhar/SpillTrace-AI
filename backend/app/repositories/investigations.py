from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.investigation import Investigation


class InvestigationRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Investigation]:
        return self.db.query(Investigation).offset(skip).limit(limit).all()

    def get_by_id(self, investigation_id: str) -> Optional[Investigation]:
        return self.db.query(Investigation).filter(Investigation.id == investigation_id).first()

    def get_by_reference_code(self, code: str) -> Optional[Investigation]:
        return self.db.query(Investigation).filter(Investigation.reference_code == code).first()

    def count(self) -> int:
        return self.db.query(Investigation).count()

    def create(self, investigation: Investigation) -> Investigation:
        self.db.add(investigation)
        self.db.commit()
        self.db.refresh(investigation)
        return investigation

    def update(self, investigation: Investigation) -> Investigation:
        self.db.commit()
        self.db.refresh(investigation)
        return investigation

    def get_by_status(self, status: str) -> List[Investigation]:
        return self.db.query(Investigation).filter(Investigation.status == status).all()
