"""
Test configuration and fixtures
"""

import pytest
from fastapi.testclient import TestClient
from src.api.main import app


@pytest.fixture
def test_client():
    """
    FastAPI test client fixture
    """
    return TestClient(app)


@pytest.fixture
def sample_brain_tumor_request():
    """
    Sample brain tumor request for testing
    """
    # Small 1x1 pixel image in base64
    return {
        "image_base64": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
    }


@pytest.fixture
def sample_heart_disease_request():
    """
    Sample heart disease request for testing
    """
    return {
        "age": 63,
        "sex": 1,
        "cp": 3,
        "trestbps": 145,
        "chol": 233,
        "fbs": 1,
        "restecg": 0,
        "thalach": 150,
        "exang": 0,
        "oldpeak": 2.3,
        "slope": 0,
        "ca": 0,
        "thal": 1
    }


@pytest.fixture
def sample_diabetes_request():
    """
    Sample diabetes request for testing
    """
    return {
        "pregnancies": 6,
        "glucose": 148,
        "blood_pressure": 72,
        "skin_thickness": 35,
        "insulin": 0,
        "bmi": 33.6,
        "diabetes_pedigree_function": 0.627,
        "age": 50
    }
