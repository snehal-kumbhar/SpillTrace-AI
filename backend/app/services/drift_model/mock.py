"""Mock Lagrangian drift model. Replace with OceanParcels-based implementation."""
import math
import random
from datetime import datetime, timedelta
from typing import Dict, Any
from app.services.drift_model.base import DriftModel


class MockDriftModel(DriftModel):

    def simulate_backward(self, spill_lat: float, spill_lon: float,
                           detected_at: str, hours: float = 8.0,
                           particle_count: int = 500,
                           config: Dict[str, Any] = None) -> Dict[str, Any]:
        config = config or {}
        wind_speed = config.get("wind_speed_ms", random.uniform(5.0, 14.0))
        wind_dir = config.get("wind_direction_deg", random.uniform(200.0, 320.0))
        current_speed = config.get("current_speed_ms", random.uniform(0.2, 0.8))
        current_dir = config.get("current_direction_deg", random.uniform(260.0, 340.0))

        # Simple analytical backward advection
        wind_rad = math.radians(wind_dir)
        current_rad = math.radians(current_dir)
        windage = 0.035  # 3.5% windage factor for oil
        total_h = hours

        dlat = -(current_speed * math.cos(current_rad) * total_h * 3600 / 111320
                 + wind_speed * windage * math.cos(wind_rad) * total_h * 3600 / 111320)
        dlon = -(current_speed * math.sin(current_rad) * total_h * 3600 /
                 (111320 * math.cos(math.radians(spill_lat)))
                 + wind_speed * windage * math.sin(wind_rad) * total_h * 3600 /
                 (111320 * math.cos(math.radians(spill_lat))))

        origin_lat = round(spill_lat + dlat + random.uniform(-0.02, 0.02), 5)
        origin_lon = round(spill_lon + dlon + random.uniform(-0.02, 0.02), 5)

        detected_dt = datetime.fromisoformat(detected_at.replace("Z", ""))
        origin_end = detected_dt - timedelta(hours=hours * 0.6)
        origin_start = origin_end - timedelta(minutes=55)

        uncertainty_km = round(random.uniform(5.0, 12.0), 1)
        probability = round(random.uniform(0.70, 0.88), 2)

        # Build probability zones as simple scaled ellipses
        def ellipse(lat, lon, r_lat, r_lon, n=20):
            return [
                [round(lon + r_lon * math.cos(2 * math.pi * i / n), 5),
                 round(lat + r_lat * math.sin(2 * math.pi * i / n), 5)]
                for i in range(n)
            ]

        prob_zones = {
            "high": ellipse(origin_lat, origin_lon, 0.035, 0.045),
            "medium": ellipse(origin_lat, origin_lon, 0.075, 0.095),
            "low": ellipse(origin_lat, origin_lon, 0.13, 0.165),
        }

        # Generate simplified particle tracks
        tracks = []
        for _ in range(min(n_tracks := 10, particle_count)):
            jlat = random.uniform(-0.04, 0.04)
            jlon = random.uniform(-0.04, 0.04)
            pts = []
            for step in range(9):
                frac = step / 8
                lat = spill_lat + frac * (origin_lat - spill_lat) + jlat * (1 - frac)
                lon = spill_lon + frac * (origin_lon - spill_lon) + jlon * (1 - frac)
                pts.append({
                    "lat": round(lat, 4), "lon": round(lon, 4),
                    "timestamp": (detected_dt - timedelta(hours=total_h * (1 - frac))).isoformat(),
                    "probability": round(probability - frac * 0.1 + random.uniform(-0.04, 0.04), 2),
                })
            tracks.append(pts)

        return {
            "origin_lat": origin_lat,
            "origin_lon": origin_lon,
            "origin_uncertainty_km": uncertainty_km,
            "origin_probability": probability,
            "origin_time_start": origin_start.isoformat(),
            "origin_time_end": origin_end.isoformat(),
            "probability_zones": prob_zones,
            "particle_tracks": tracks,
            "wind_speed_ms": round(wind_speed, 1),
            "wind_direction_deg": round(wind_dir, 1),
            "current_speed_ms": round(current_speed, 2),
            "current_direction_deg": round(current_dir, 1),
            "model": "MockDriftModel v1.0 (replace with OceanParcels Lagrangian simulation)",
            "is_simulated": True,
        }
