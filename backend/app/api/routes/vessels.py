from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.repositories.vessels import VesselRepository
from app.schemas.vessel import VesselOut, VesselListOut, VesselWithTrajectoryOut, TrajectoryPointOut

router = APIRouter(prefix="/vessels", tags=["Vessels"])


@router.get("", response_model=VesselListOut)
def list_vessels(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    repo = VesselRepository(db)
    items = repo.get_all(skip=skip, limit=limit)
    return VesselListOut(items=items, total=repo.count())


@router.get("/{vessel_id}", response_model=VesselOut)
def get_vessel(vessel_id: str, db: Session = Depends(get_db)):
    repo = VesselRepository(db)
    vessel = repo.get_by_id(vessel_id)
    if not vessel:
        raise HTTPException(status_code=404, detail="Vessel not found")
    return vessel


@router.get("/{vessel_id}/trajectory", response_model=VesselWithTrajectoryOut)
def get_vessel_trajectory(vessel_id: str, db: Session = Depends(get_db)):
    repo = VesselRepository(db)
    vessel = repo.get_by_id(vessel_id)
    if not vessel:
        raise HTTPException(status_code=404, detail="Vessel not found")
    trajectory = repo.get_trajectory(vessel_id)
    out = VesselWithTrajectoryOut.model_validate(vessel)
    out.trajectories = [TrajectoryPointOut.model_validate(t) for t in trajectory]
    return out
