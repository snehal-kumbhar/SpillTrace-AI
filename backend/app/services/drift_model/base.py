"""
DriftModel abstraction.
Replace MockDriftModel with LagrangianDriftModel (OceanParcels) when ready.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any


class DriftModel(ABC):
    """Interface for Lagrangian particle drift simulation."""

    @abstractmethod
    def simulate_backward(self, spill_lat: float, spill_lon: float,
                           detected_at: str, hours: float,
                           particle_count: int, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run backward drift simulation from observed spill location.

        Returns:
            Dict with keys: origin_lat, origin_lon, origin_uncertainty_km,
            origin_probability, origin_time_start, origin_time_end,
            probability_zones, particle_tracks, env_metadata
        """
        ...
