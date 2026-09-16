"""Mock attribution engine. Replace with XGBoost/ensemble model."""
import random
import math
from typing import List, Dict, Any
from app.services.attribution.base import AttributionEngine


class MockAttributionEngine(AttributionEngine):

    def analyze(self, investigation_id: str,
                drift_result: Dict[str, Any],
                candidate_vessels: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        origin_lat = drift_result.get("origin_lat", 0)
        origin_lon = drift_result.get("origin_lon", 0)
        scored = []

        for i, v in enumerate(candidate_vessels):
            # Simulate distance-based scoring with noise
            vlat = v.get("current_lat", origin_lat + random.uniform(-0.5, 0.5))
            vlon = v.get("current_lon", origin_lon + random.uniform(-0.5, 0.5))
            dist = math.sqrt((vlat - origin_lat) ** 2 + (vlon - origin_lon) ** 2) * 111
            proximity = max(10.0, 100.0 - dist * 4.0 + random.uniform(-5, 5))
            temporal = round(random.uniform(60, 95), 1)
            drift_c = round(random.uniform(55, 96), 1)
            traj = round(random.uniform(50, 94), 1)
            behaviour = round(random.uniform(45, 88), 1)
            cf = round(random.uniform(40, 94), 1)
            overall = round((temporal * 0.18 + proximity * 0.22 + drift_c * 0.20
                             + traj * 0.17 + behaviour * 0.10 + cf * 0.13), 1)
            conf = "High" if overall >= 75 else "Medium" if overall >= 50 else "Low"

            scored.append({
                "vessel_id": v["id"],
                "rank": 0,
                "overall_score": overall,
                "confidence_level": conf,
                "temporal_compatibility": temporal,
                "spatial_proximity": round(proximity, 1),
                "drift_consistency": drift_c,
                "trajectory_compatibility": traj,
                "behaviour_anomaly": behaviour,
                "counterfactual_similarity": cf,
                "evidence_bullets": [
                    f"Vessel was {round(dist, 1)} km from the estimated origin zone.",
                    f"Temporal analysis: vessel was in the area during the estimated spill window.",
                    f"Drift consistency score: {drift_c}% — moderate alignment with backward drift vector.",
                    f"No significant speed anomaly detected." if behaviour < 70 else
                    f"AIS anomaly detected: speed reduction during spill window.",
                    f"Counterfactual simulation spatial overlap: {cf:.1f}%.",
                ],
                "evidence_strength": "Strong" if overall >= 75 else "Moderate" if overall >= 50 else "Weak",
                "counterfactual_spatial_overlap_pct": round(cf * 0.92 + random.uniform(-3, 3), 1),
                "counterfactual_centroid_error_km": round(max(1.0, dist * 0.3 + random.uniform(0, 5)), 1),
                "counterfactual_shape_similarity": round(cf * 0.88 + random.uniform(-4, 4), 1),
                "counterfactual_temporal_consistency": round(temporal * 0.95 + random.uniform(-3, 3), 1),
                "counterfactual_overall_similarity": round(overall * 0.95 + random.uniform(-2, 2), 1),
                "is_simulated": True,
            })

        scored.sort(key=lambda x: x["overall_score"], reverse=True)
        for i, s in enumerate(scored):
            s["rank"] = i + 1
        return scored
