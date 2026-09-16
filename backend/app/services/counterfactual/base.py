"""
CounterfactualSimulator abstraction.
Replace MockSimulator with OceanDriftSimulator when integrating real forward drift.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any


class CounterfactualSimulator(ABC):
    @abstractmethod
    def simulate_forward(self, vessel_lat: float, vessel_lon: float,
                          vessel_time: str, hours: float,
                          config: Dict[str, Any]) -> Dict[str, Any]:
        """Forward drift simulation from a vessel position."""
        ...


class MockCounterfactualSimulator(CounterfactualSimulator):
    def simulate_forward(self, vessel_lat: float, vessel_lon: float,
                          vessel_time: str, hours: float = 6.0,
                          config: Dict[str, Any] = None) -> Dict[str, Any]:
        import math, random
        config = config or {}
        wind_dir = config.get("wind_direction_deg", 245.0)
        current_dir = config.get("current_direction_deg", 310.0)
        wind_speed = config.get("wind_speed_ms", 8.2)
        current_speed = config.get("current_speed_ms", 0.45)

        wind_rad = math.radians(wind_dir)
        current_rad = math.radians(current_dir)
        windage = 0.035
        h = hours

        dlat = (current_speed * math.cos(current_rad) * h * 3600 / 111320
                + wind_speed * windage * math.cos(wind_rad) * h * 3600 / 111320)
        dlon = (current_speed * math.sin(current_rad) * h * 3600 /
                (111320 * math.cos(math.radians(vessel_lat)))
                + wind_speed * windage * math.sin(wind_rad) * h * 3600 /
                (111320 * math.cos(math.radians(vessel_lat))))

        sim_lat = round(vessel_lat + dlat + random.uniform(-0.01, 0.01), 5)
        sim_lon = round(vessel_lon + dlon + random.uniform(-0.01, 0.01), 5)
        spatial_overlap = round(random.uniform(65.0, 88.0), 1)

        return {
            "simulated_center_lat": sim_lat,
            "simulated_center_lon": sim_lon,
            "spatial_overlap_pct": spatial_overlap,
            "centroid_error_km": round(random.uniform(2.0, 8.0), 1),
            "shape_similarity": round(spatial_overlap * 0.92 + random.uniform(-4, 4), 1),
            "temporal_consistency": round(random.uniform(82.0, 96.0), 1),
            "overall_similarity": round(spatial_overlap * 0.97 + random.uniform(-2, 2), 1),
            "model": "MockCounterfactualSimulator v1.0",
            "is_simulated": True,
        }
