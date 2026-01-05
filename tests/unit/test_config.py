"""
Unit tests for configuration management
"""

import pytest
from config.settings import get_settings


@pytest.mark.unit
def test_settings_singleton():
    """Test that settings returns the same instance"""
    settings1 = get_settings()
    settings2 = get_settings()
    assert settings1 is settings2


@pytest.mark.unit
def test_default_settings():
    """Test default configuration values"""
    settings = get_settings()
    assert settings.app_name == "OpenHealth AI Service"
    assert settings.port == 8000
    assert settings.confidence_threshold == 0.75
    assert settings.model_version == "v1"


@pytest.mark.unit
def test_settings_types():
    """Test that settings have correct types"""
    settings = get_settings()
    assert isinstance(settings.port, int)
    assert isinstance(settings.confidence_threshold, float)
    assert isinstance(settings.debug, bool)
    assert isinstance(settings.monitoring_enabled, bool)
