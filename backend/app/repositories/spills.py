from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.spill import SpillEvent, SpillDetection


class SpillRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> List[SpillEvent]:
        return self.db.query(SpillEvent).offset(skip).limit(limit).all()

    def get_by_id(self, spill_id: str) -> Optional[SpillEvent]:
        return (
            self.db.query(SpillEvent)
            .filter(SpillEvent.id == spill_id)
            .first()
        )

    def get_by_investigation(self, investigation_id: str) -> List[SpillEvent]:
        return (
            self.db.query(SpillEvent)
            .filter(SpillEvent.investigation_id == investigation_id)
            .all()
        )

    def count(self) -> int:
        return self.db.query(SpillEvent).count()

    def create(self, spill: SpillEvent, detection: SpillDetection) -> SpillEvent:
        self.db.add(spill)
        self.db.add(detection)
        self.db.commit()
        self.db.refresh(spill)
        return spill
