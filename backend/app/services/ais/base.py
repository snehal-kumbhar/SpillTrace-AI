"""AIS data service abstraction. Replace with Spire/exactEarth API integration."""
from abc import ABC, abstractmethod
from typing import List, Dict, Any


class AISService(ABC):
    @abstractmethod
    def get_vessels_in_area(self, lat: float, lon: float,
                             radius_km: float, time_start: str,
                             time_end: str) -> List[Dict[str, Any]]:
        """Fetch vessels from AIS within a geographic radius and time window."""
        ...


class MockAISService(AISService):
    """Returns candidate vessels from local DB — future: query real AIS API."""

    def __init__(self, vessel_repo=None):
        self.vessel_repo = vessel_repo

    def get_vessels_in_area(self, lat: float, lon: float,
                             radius_km: float = 50.0,
                             time_start: str = "", time_end: str = "") -> List[Dict[str, Any]]:
        if self.vessel_repo:
            vessels = self.vessel_repo.get_all()
            return [
                {
                    "id": v.id, "name": v.name, "imo": v.imo,
                    "current_lat": v.current_lat, "current_lon": v.current_lon,
                    "vessel_type": v.vessel_type,
                }
                for v in vessels
            ]
        return []
