from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.vessel import Vessel, VesselTrajectoryPoint


class VesselRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Vessel]:
        return self.db.query(Vessel).offset(skip).limit(limit).all()

    def get_by_id(self, vessel_id: str) -> Optional[Vessel]:
        return self.db.query(Vessel).filter(Vessel.id == vessel_id).first()

    def get_by_imo(self, imo: str) -> Optional[Vessel]:
        return self.db.query(Vessel).filter(Vessel.imo == imo).first()

    def count(self) -> int:
        return self.db.query(Vessel).count()

    def get_trajectory(self, vessel_id: str, limit: int = 200) -> List[VesselTrajectoryPoint]:
        return (
            self.db.query(VesselTrajectoryPoint)
            .filter(VesselTrajectoryPoint.vessel_id == vessel_id)
            .order_by(VesselTrajectoryPoint.timestamp.desc())
            .limit(limit)
            .all()
        )

    def get_all_with_trajectories(self) -> List[Vessel]:
        return self.db.query(Vessel).all()
