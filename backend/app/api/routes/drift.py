from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.repositories.investigations import InvestigationRepository
from app.repositories.spills import SpillRepository
from app.repositories.evidence import DriftRepository
from app.models.drift import DriftSimulation
from app.schemas.drift import DriftSimulationOut, DriftSimulateRequest
from app.services.factory import get_drift_model

router = APIRouter(prefix="/drift", tags=["Drift Analysis"])


@router.post("/simulate", response_model=DriftSimulationOut, status_code=201)
def simulate_drift(payload: DriftSimulateRequest, db: Session = Depends(get_db)):
    inv_repo = InvestigationRepository(db)
    spill_repo = SpillRepository(db)
    drift_repo = DriftRepository(db)

    inv = inv_repo.get_by_id(payload.investigation_id)
    if not inv:
        raise HTTPException(status_code=404, detail="Investigation not found")

    spills = spill_repo.get_by_investigation(inv.id)
    spill = spills[0] if spills else None
    spill_lat = spill.center_lat if spill else inv.center_lat
    spill_lon = spill.center_lon if spill else inv.center_lon
    detected_at = (spill.detected_at if spill else inv.detection_time).isoformat()

    model = get_drift_model()
    result = model.simulate_backward(
        spill_lat, spill_lon, detected_at,
        hours=payload.total_hours,
        particle_count=payload.particle_count,
        config={},
    )

    sim = DriftSimulation(
        investigation_id=inv.id,
        simulation_type="backward",
        model_version=result.get("model", "mock-v1.0"),
        particle_count=payload.particle_count,
        total_hours=payload.total_hours,
        origin_lat=result["origin_lat"],
        origin_lon=result["origin_lon"],
        origin_uncertainty_km=result["origin_uncertainty_km"],
        origin_probability=result["origin_probability"],
        origin_time_start=datetime.fromisoformat(result["origin_time_start"]),
        origin_time_end=datetime.fromisoformat(result["origin_time_end"]),
        probability_zones=result["probability_zones"],
        particle_tracks=result["particle_tracks"],
        wind_speed_ms=result["wind_speed_ms"],
        wind_direction_deg=result["wind_direction_deg"],
        current_speed_ms=result["current_speed_ms"],
        current_direction_deg=result["current_direction_deg"],
        is_simulated=True,
    )
    return drift_repo.create(sim)


@router.get("/{drift_id}", response_model=DriftSimulationOut)
def get_drift(drift_id: str, db: Session = Depends(get_db)):
    repo = DriftRepository(db)
    sim = repo.get_by_id(drift_id)
    if not sim:
        raise HTTPException(status_code=404, detail="Drift simulation not found")
    return sim
