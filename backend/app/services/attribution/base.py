"""
AttributionEngine abstraction.
Replace MockAttributionEngine with MultiEvidenceAttributionEngine (XGBoost/ensemble).
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any


class AttributionEngine(ABC):
    """Interface for multi-evidence vessel attribution scoring."""

    @abstractmethod
    def analyze(self, investigation_id: str,
                drift_result: Dict[str, Any],
                candidate_vessels: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Score candidate vessels against the drift/spill evidence.

        Returns:
            List of candidate dicts sorted by overall_score desc, each with:
                vessel_id, rank, overall_score, confidence_level,
                sub-scores, evidence_bullets, evidence_strength,
                counterfactual metrics
        """
        ...
