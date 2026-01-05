"""
Health check and monitoring endpoints
"""

from fastapi import APIRouter, status
from datetime import datetime
from src.api.schemas import HealthCheckResponse, ModelInfoResponse, ModelInfo
from src.models.registry import model_registry
from src.models.loader import model_loader
from src.monitoring.metrics import metrics_collector
from config.settings import get_settings

router = APIRouter(tags=["Health & Monitoring"])


@router.get(
    "/health",
    response_model=HealthCheckResponse,
    status_code=status.HTTP_200_OK,
    summary="Health check endpoint"
)
async def health_check():
    """
    Health check endpoint - returns service status
    Used by orchestrators and load balancers
    """
    settings = get_settings()
    return HealthCheckResponse(
        status="healthy",
        version=settings.app_version,
        timestamp=datetime.utcnow()
    )


@router.get(
    "/ready",
    response_model=HealthCheckResponse,
    status_code=status.HTTP_200_OK,
    summary="Readiness check endpoint"
)
async def readiness_check():
    """
    Readiness check - verifies service is ready to handle requests
    """
    settings = get_settings()
    
    # Could add additional checks here (database connection, etc.)
    return HealthCheckResponse(
        status="ready",
        version=settings.app_version,
        timestamp=datetime.utcnow()
    )


@router.get(
    "/model-info",
    response_model=ModelInfoResponse,
    status_code=status.HTTP_200_OK,
    summary="Get model information"
)
async def get_model_info():
    """
    Returns information about all loaded models
    Including versions, metadata, and capabilities
    """
    settings = get_settings()
    models_info = model_registry.list_all_models()
    
    model_list = []
    for model in models_info:
        model_list.append(ModelInfo(
            name=model["name"],
            version=model["active_version"],
            type=model["metadata"].get("model_type", "unknown"),
            loaded=model["loaded"],
            confidence_threshold=settings.confidence_threshold
        ))
    
    return ModelInfoResponse(
        models=model_list,
        active_version=settings.model_version,
        total_models=len(model_list)
    )


@router.get(
    "/metrics",
    summary="Get service metrics",
    tags=["Monitoring"]
)
async def get_metrics():
    """
    Returns collected metrics including latencies, prediction counts, and confidence stats
    """
    return metrics_collector.get_all_metrics()
