from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.repositories.spills import SpillRepository
from app.repositories.investigations import InvestigationRepository
from app.models.spill import SpillEvent, SpillDetection
from app.schemas.spill import SpillEventOut, SpillListOut, DetectRequest
from app.services.factory import get_spill_detector

router = APIRouter(prefix="/spills", tags=["Spills"])


@router.get("", response_model=SpillListOut)
def list_spills(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    repo = SpillRepository(db)
    items = repo.get_all(skip=skip, limit=limit)
    return SpillListOut(items=items, total=repo.count())


@router.get("/{spill_id}", response_model=SpillEventOut)
def get_spill(spill_id: str, db: Session = Depends(get_db)):
    repo = SpillRepository(db)
    spill = repo.get_by_id(spill_id)
    if not spill:
        raise HTTPException(status_code=404, detail="Spill event not found")
    return spill


@router.post("/detect", response_model=SpillEventOut, status_code=201)
def detect_spill(payload: DetectRequest, db: Session = Depends(get_db)):
    inv_repo = InvestigationRepository(db)
    spill_repo = SpillRepository(db)

    inv = inv_repo.get_by_id(payload.investigation_id)
    if not inv:
        raise HTTPException(status_code=404, detail="Investigation not found")

    detector = get_spill_detector()
    result = detector.detect(
        payload.image_url or "mock://sar/sentinel-1a",
        {"center_lat": inv.center_lat, "center_lon": inv.center_lon},
    )

    spill = SpillEvent(
        investigation_id=inv.id,
        name=f"Detected Slick — {inv.reference_code}",
        detected_at=datetime.utcnow(),
        center_lat=inv.center_lat,
        center_lon=inv.center_lon,
        polygon_coordinates=result["polygon_coordinates"],
        area_km2=result["area_km2"],
        estimated_volume_m3=result.get("estimated_volume_m3", 500.0),
    )
    look_alike = result.get("look_alike_rejection", {})
    detection = SpillDetection(
        spill_id="pending",
        acquisition_time=datetime.utcnow(),
        confidence=result["confidence"],
        mean_backscatter_db=result.get("mean_backscatter_db", -24.0),
        ambient_backscatter_db=result.get("ambient_backscatter_db", -14.0),
        contrast_db=result.get("contrast_db", -10.0),
        incidence_angle_deg=result.get("incidence_angle_deg", 36.4),
        biogenic_slick_rejection=look_alike.get("biogenic_slick", 95.0),
        low_wind_calm_rejection=look_alike.get("low_wind_calm", 92.0),
        internal_wave_rejection=look_alike.get("internal_wave", 98.0),
        rain_cell_rejection=look_alike.get("rain_cell", 95.0),
        sar_preview_url=payload.image_url,
    )
    return spill_repo.create(spill, detection)
