"""Service factory — returns mock or real implementations based on config."""
from app.core.config import settings
from app.services.spill_detection.mock import MockSpillDetector
from app.services.drift_model.mock import MockDriftModel
from app.services.attribution.mock import MockAttributionEngine
from app.services.counterfactual.base import MockCounterfactualSimulator
from app.services.reporting.mock import MockReportGenerator


def get_spill_detector():
    if settings.USE_MOCK_MODELS:
        return MockSpillDetector()
    raise NotImplementedError("DeepLearningSpillDetector not yet implemented")


def get_drift_model():
    if settings.USE_MOCK_MODELS:
        return MockDriftModel()
    raise NotImplementedError("OceanParcelsDriftModel not yet implemented")


def get_attribution_engine():
    if settings.USE_MOCK_MODELS:
        return MockAttributionEngine()
    raise NotImplementedError("MultiEvidenceAttributionEngine not yet implemented")


def get_counterfactual_simulator():
    if settings.USE_MOCK_MODELS:
        return MockCounterfactualSimulator()
    raise NotImplementedError("OceanDriftSimulator not yet implemented")


def get_report_generator():
    if settings.USE_MOCK_MODELS:
        return MockReportGenerator()
    raise NotImplementedError("PDFReportGenerator not yet implemented")
