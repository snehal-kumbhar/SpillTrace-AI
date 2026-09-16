import math
from typing import List, Tuple, Dict, Any

def haversine_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate the great circle distance in kilometers between two points."""
    R = 6371.0  # Earth's radius in km
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (math.sin(delta_phi / 2.0) ** 2 +
         math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2)
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return R * c

def haversine_distance_nm(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance in nautical miles."""
    return haversine_distance_km(lat1, lon1, lat2, lon2) * 0.539957

def calculate_polygon_centroid(coords: List[List[float]]) -> Tuple[float, float]:
    """Calculate centroid (lat, lon) from a list of [lon, lat] or [lat, lon] pairs."""
    if not coords:
        return (0.0, 0.0)
    # GeoJSON coordinates are usually [longitude, latitude]
    total_lon = sum(pt[0] for pt in coords)
    total_lat = sum(pt[1] for pt in coords)
    n = len(coords)
    return (round(total_lat / n, 5), round(total_lon / n, 5))

def calculate_bounding_box(coords: List[List[float]]) -> Dict[str, float]:
    """Return min_lat, min_lon, max_lat, max_lon."""
    lons = [pt[0] for pt in coords]
    lats = [pt[1] for pt in coords]
    return {
        "min_lon": min(lons),
        "min_lat": min(lats),
        "max_lon": max(lons),
        "max_lat": max(lats)
    }

def calculate_bearing(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate initial compass bearing in degrees from point 1 to point 2."""
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_lon = math.radians(lon2 - lon1)

    y = math.sin(delta_lon) * math.cos(phi2)
    x = math.cos(phi1) * math.sin(phi2) - math.sin(phi1) * math.cos(phi2) * math.cos(delta_lon)
    bearing = math.degrees(math.atan2(y, x))
    return (bearing + 360.0) % 360.0
