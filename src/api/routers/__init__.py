"""
Router initialization
"""

from src.api.routers.health import router as health_router
from src.api.routers.predictions import router as predictions_router
from src.api.routers.admin import router as admin_router
from src.api.routers.working_predictions import router as working_predictions_router
from src.api.routers.extended_predictions import router as extended_predictions_router

__all__ = ["health_router", "predictions_router", "admin_router", "working_predictions_router", "extended_predictions_router"]
