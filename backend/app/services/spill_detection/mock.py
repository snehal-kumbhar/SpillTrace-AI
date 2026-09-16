"""Mock implementation of SpillDetector. Replace with DeepLearningSpillDetector."""
import math
import random
from typing import Dict, Any
from app.services.spill_detection.base import SpillDetector


class MockSpillDetector(SpillDetector):
    """Simulates a deep-learning SAR oil spill detector."""

    def detect(self, image_path: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        base_lat = metadata.get("center_lat", 18.42)
        base_lon = metadata.get("center_lon", 67.21)
        confidence = round(random.uniform(88.0, 97.5), 1)
        area = round(random.uniform(8.0, 28.0), 1)
        polygon = self._generate_ellipse(base_lat, base_lon, 0.07, 0.11)
        return {
            "confidence": confidence,
            "area_km2": area,
            "estimated_volume_m3": round(area * 33.5, 1),
            "polygon_coordinates": polygon,
            "mean_backscatter_db": round(random.uniform(-26.0, -22.0), 1),
            "ambient_backscatter_db": round(random.uniform(-16.0, -12.0), 1),
            "contrast_db": round(random.uniform(-12.0, -8.0), 1),
            "incidence_angle_deg": round(metadata.get("incidence_angle", 36.4), 1),
            "polarization": "VV+VH",
            "look_alike_rejection": {
                "biogenic_slick": round(random.uniform(92.0, 99.0), 1),
                "low_wind_calm": round(random.uniform(88.0, 97.0), 1),
                "internal_wave": round(random.uniform(94.0, 99.5), 1),
                "rain_cell": round(random.uniform(91.0, 98.0), 1),
            },
            "model": "MockSpillDetector v1.0 (simulated — replace with U-Net/DeepLabV3+)",
            "is_simulated": True,
        }

    @staticmethod
    def _generate_ellipse(lat: float, lon: float,
                           lat_r: float, lon_r: float, n: int = 18) -> list:
        return [
            [round(lon + lon_r * math.cos(2 * math.pi * i / n), 5),
             round(lat + lat_r * math.sin(2 * math.pi * i / n), 5)]
            for i in range(n)
        ] + [[round(lon + lon_r, 5), round(lat, 5)]]
