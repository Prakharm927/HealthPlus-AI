"""
Admin endpoints for model management
"""

from fastapi import APIRouter, HTTPException, status
from src.models.registry import model_registry
from src.models.loader import model_loader
from src.monitoring.logger import logger

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.post(
    "/reload-model/{model_name}",
    summary="Reload a specific model",
    status_code=status.HTTP_200_OK
)
async def reload_model(model_name: str):
    """
    Force reload a specific model
    Clears cache and reloads from disk
    """
    try:
        version = model_registry.get_active_version(model_name)
        model_loader.reload_model(model_name, version)
        
        logger.info(f"Reloaded model: {model_name} v{version}")
        
        return {
            "status": "success",
            "message": f"Reloaded {model_name} version {version}",
            "model": model_name,
            "version": version
        }
    except Exception as e:
        logger.error(f"Failed to reload {model_name}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to reload model: {str(e)}"
        )


@router.post(
    "/rollback/{model_name}",
    summary="Rollback model to previous version",
    status_code=status.HTTP_200_OK
)
async def rollback_model(model_name: str):
    """
    Rollback a model to its previous version
    Useful for quick revert in case of issues
    """
    try:
        old_version = model_registry.get_active_version(model_name)
        new_version = model_registry.rollback(model_name)
        
        if new_version is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot rollback {model_name}: insufficient versions"
            )
        
        # Clear cache to force reload with new version
        model_loader.clear_cache()
        
        logger.info(f"Rolled back {model_name}: {old_version} -> {new_version}")
        
        return {
            "status": "success",
            "message": f"Rolled back {model_name}",
            "model": model_name,
            "old_version": old_version,
            "new_version": new_version
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to rollback {model_name}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to rollback model: {str(e)}"
        )


@router.post(
    "/set-version/{model_name}/{version}",
    summary="Set specific model version",
    status_code=status.HTTP_200_OK
)
async def set_model_version(model_name: str, version: str):
    """
    Set a specific version for a model
    """
    try:
        # Verify version exists
        available_versions = model_registry.get_available_versions(model_name)
        if version not in available_versions:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Version {version} not found for {model_name}. Available: {available_versions}"
            )
        
        old_version = model_registry.get_active_version(model_name)
        model_registry.set_active_version(model_name, version)
        
        # Clear cache to force reload
        model_loader.clear_cache()
        
        logger.info(f"Version switch for {model_name}: {old_version} -> {version}")
        
        return {
            "status": "success",
            "message": f"Switched {model_name} to version {version}",
            "model": model_name,
            "old_version": old_version,
            "new_version": version
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to set version for {model_name}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to set version: {str(e)}"
        )


@router.get(
    "/cache-info",
    summary="Get model cache information",
    status_code=status.HTTP_200_OK
)
async def get_cache_info():
    """
    Get information about cached models
    """
    return model_loader.get_cache_info()


@router.post(
    "/clear-cache",
    summary="Clear model cache",
    status_code=status.HTTP_200_OK
)
async def clear_cache():
    """
    Clear all models from cache
    Models will be reloaded on next prediction request
    """
    model_loader.clear_cache()
    logger.info("Cleared model cache")
    
    return {
        "status": "success",
        "message": "Model cache cleared"
    }
