"""
Integration tests for API endpoints
"""

import pytest
from fastapi.testclient import TestClient


@pytest.mark.integration
def test_health_endpoint(test_client: TestClient):
    """Test health check endpoint"""
    response = test_client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data


@pytest.mark.integration
def test_readiness_endpoint(test_client: TestClient):
    """Test readiness check endpoint"""
    response = test_client.get("/ready")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ready"


@pytest.mark.integration
def test_model_info_endpoint(test_client: TestClient):
    """Test model info endpoint"""
    response = test_client.get("/model-info")
    assert response.status_code == 200
    data = response.json()
    assert "models" in data
    assert "total_models" in data
    assert isinstance(data["models"], list)


@pytest.mark.integration
def test_metrics_endpoint(test_client: TestClient):
    """Test metrics endpoint"""
    response = test_client.get("/metrics")
    assert response.status_code == 200
    data = response.json()
    assert "latencies" in data
    assert "predictions" in data


@pytest.mark.integration
def test_root_endpoint(test_client: TestClient):
    """Test root endpoint"""
    response = test_client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "service" in data
    assert "version" in data


@pytest.mark.integration
def test_openapi_docs(test_client: TestClient):
    """Test that OpenAPI docs are accessible"""
    response = test_client.get("/docs")
    assert response.status_code == 200
    
    response = test_client.get("/openapi.json")
    assert response.status_code == 200
