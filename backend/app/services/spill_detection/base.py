"""
SpillDetector abstraction.
Implement DeepLearningSpillDetector here when integrating PyTorch / U-Net / DeepLabV3+.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any


class SpillDetector(ABC):
    """Interface for SAR oil spill detection models."""

    @abstractmethod
    def detect(self, image_path: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run spill detection on a SAR image.

        Args:
            image_path: Local path or URI to the SAR image.
            metadata: SAR acquisition metadata (incidence angle, polarization, etc.)

        Returns:
            Detection result dict with keys:
                - confidence (float 0–100)
                - area_km2 (float)
                - polygon_coordinates (list of [lon, lat])
                - mean_backscatter_db (float)
                - look_alike_rejection (dict)
        """
        ...
