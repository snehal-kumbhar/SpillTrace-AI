from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.repositories.investigations import InvestigationRepository
from app.repositories.vessels import VesselRepository
from app.repositories.evidence import AttributionRepository, DriftRepository
from app.models.attribution import AttributionResult, CandidateVesselMatch
from app.schemas.attribution import AttributionResultOut, CandidateVesselMatchOut, AttributionAnalyzeRequest
from app.services.factory import get_attribution_engine

router = APIRouter(prefix="/attribution", tags=["Attribution"])


def _enrich_candidate(c: CandidateVesselMatch) -> CandidateVesselMatchOut:
    out = CandidateVesselMatchOut.model_validate(c)
    if c.vessel:
        out.vessel_name = c.vessel.name
        out.vessel_imo = c.vessel.imo
        out.vessel_type = c.vessel.vessel_type
        out.vessel_flag = c.vessel.flag
    return out


@router.post("/analyze", response_model=AttributionResultOut, status_code=201)
def analyze_attribution(payload: AttributionAnalyzeRequest, db: Session = Depends(get_db)):
    inv_repo = InvestigationRepository(db)
    vessel_repo = VesselRepository(db)
    drift_repo = DriftRepository(db)
    attr_repo = AttributionRepository(db)

    inv = inv_repo.get_by_id(payload.investigation_id)
    if not inv:
        raise HTTPException(status_code=404, detail="Investigation not found")

    drift = drift_repo.get_by_investigation(inv.id)
    drift_result = {
        "origin_lat": drift.origin_lat if drift else inv.center_lat,
        "origin_lon": drift.origin_lon if drift else inv.center_lon,
    }

    vessels = vessel_repo.get_all(limit=20)
    candidate_data = [
        {"id": v.id, "current_lat": v.current_lat, "current_lon": v.current_lon}
        for v in vessels
    ]

    engine = get_attribution_engine()
    scored = engine.analyze(inv.id, drift_result, candidate_data)

    result = AttributionResult(
        investigation_id=inv.id,
        model_version="mock-attribution-v1.0",
    )
    attr_repo.create(result)

    for s in scored:
        match = CandidateVesselMatch(
            attribution_result_id=result.id,
            vessel_id=s["vessel_id"],
            rank=s["rank"],
            overall_score=s["overall_score"],
            confidence_level=s["confidence_level"],
            temporal_compatibility=s["temporal_compatibility"],
            spatial_proximity=s["spatial_proximity"],
            drift_consistency=s["drift_consistency"],
            trajectory_compatibility=s["trajectory_compatibility"],
            behaviour_anomaly=s["behaviour_anomaly"],
            counterfactual_similarity=s["counterfactual_similarity"],
            evidence_bullets=s["evidence_bullets"],
            evidence_strength=s["evidence_strength"],
            counterfactual_spatial_overlap_pct=s.get("counterfactual_spatial_overlap_pct"),
            counterfactual_centroid_error_km=s.get("counterfactual_centroid_error_km"),
            counterfactual_shape_similarity=s.get("counterfactual_shape_similarity"),
            counterfactual_temporal_consistency=s.get("counterfactual_temporal_consistency"),
            counterfactual_overall_similarity=s.get("counterfactual_overall_similarity"),
            is_simulated=True,
        )
        db.add(match)
    db.commit()
    db.refresh(result)

    out = AttributionResultOut.model_validate(result)
    out.candidates = [_enrich_candidate(c) for c in result.candidates]
    return out


@router.get("/investigations/{investigation_id}", response_model=AttributionResultOut)
def get_investigation_attribution(investigation_id: str, db: Session = Depends(get_db)):
    repo = AttributionRepository(db)
    result = repo.get_by_investigation(investigation_id)
    if not result:
        raise HTTPException(status_code=404, detail="Attribution result not found")
    out = AttributionResultOut.model_validate(result)
    out.candidates = [_enrich_candidate(c) for c in result.candidates]
    return out
