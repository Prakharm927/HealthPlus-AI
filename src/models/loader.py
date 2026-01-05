"""
Model loader with caching and lazy loading
Handles loading of TensorFlow and pickle models
"""

import pickle
from pathlib import Path
from typing import Any, Dict, Optional
from src.models.registry import model_registry
from src.monitoring.logger import logger
from config.settings import get_settings


def lazy_import_tensorflow():
    """Lazy import TensorFlow - only when loading .h5 models"""
    try:
        from tensorflow.keras.models import load_model as tf_load_model
        return tf_load_model
    except ImportError:
        logger.warning("TensorFlow not installed")
        return None


class ModelLoader:
    """
    Singleton model loader with caching
    Lazy loads models on first request and caches them
    """
    
    _instance = None
    _models_cache: Dict[str, Any] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelLoader, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.settings = get_settings()
        self.registry = model_registry
    
    def get_model(self, model_name: str, version: str = None) -> Any:
        """
        Get model from cache or load it
        
        Args:
            model_name: Name of the model
            version: Specific version (uses active version if not specified)
        
        Returns:
            Loaded model object
        
        Raises:
            FileNotFoundError: If model file doesn't exist
            Exception: If model loading fails
        """
        if version is None:
            version = self.registry.get_active_version(model_name)
        
        cache_key = f"{model_name}:{version}"
        
        # Check cache
        if cache_key in self._models_cache:
            logger.debug(f"Loading {model_name} v{version} from cache")
            return self._models_cache[cache_key]
        
        # Load model
        model_path = self.registry.get_model_path(model_name, version)
        
        if not model_path.exists():
            error_msg = f"Model file not found: {model_path}"
            logger.error(error_msg, extra={"model_name": model_name})
            raise FileNotFoundError(error_msg)
        
        try:
            logger.info(f"Loading {model_name} v{version} from {model_path}")
            
            # Load based on file extension
            if model_path.suffix == '.h5':
                tf_load_model = lazy_import_tensorflow()
                if tf_load_model is None:
                    raise RuntimeError("TensorFlow not available")
                model = tf_load_model(str(model_path))
            elif model_path.suffix == '.pkl':
                with open(model_path, 'rb') as f:
                    model = pickle.load(f)
            else:
                raise ValueError(f"Unsupported model file type: {model_path.suffix}")
            
            # Cache the model
            self._models_cache[cache_key] = model
            
            logger.info(
                f"Successfully loaded {model_name} v{version}",
                extra={"model_name": model_name}
            )
            
            return model
            
        except Exception as e:
            logger.error(
                f"Failed to load {model_name} v{version}: {e}",
                extra={"model_name": model_name},
                exc_info=True
            )
            raise
    
    def reload_model(self, model_name: str, version: str = None):
        """
        Force reload a model (clear cache and reload)
        
        Args:
            model_name: Name of the model
            version: Specific version (uses active version if not specified)
        """
        if version is None:
            version = self.registry.get_active_version(model_name)
        
        cache_key = f"{model_name}:{version}"
        
        # Clear from cache
        if cache_key in self._models_cache:
            del self._models_cache[cache_key]
            logger.info(f"Cleared cache for {model_name} v{version}")
        
        # Reload
        return self.get_model(model_name, version)
    
    def validate_model(self, model_name: str, version: str = None) -> bool:
        """
        Validate that a model can be loaded successfully
        
        Args:
            model_name: Name of the model
            version: Specific version (uses active version if not specified)
        
        Returns:
            True if model loads successfully, False otherwise
        """
        try:
            self.get_model(model_name, version)
            return True
        except Exception as e:
            logger.warning(f"Model validation failed for {model_name}: {e}")
            return False
    
    def preload_models(self, model_names: list = None):
        """
        Preload models into cache
        
        Args:
            model_names: List of model names to preload (preloads all if None)
        """
        if model_names is None:
            model_names = [
                "brain_tumor",
                "kidney",
                "liver",
                "heart",
                "diabetes",
                "breast_cancer",
                "parkinsons"
            ]
        
        for model_name in model_names:
            try:
                self.get_model(model_name)
                logger.info(f"Preloaded {model_name}")
            except Exception as e:
                logger.warning(f"Failed to preload {model_name}: {e}")
    
    def clear_cache(self):
        """Clear all cached models"""
        count = len(self._models_cache)
        self._models_cache.clear()
        logger.info(f"Cleared {count} models from cache")
    
    def get_cache_info(self) -> Dict:
        """Get information about cached models"""
        return {
            "cached_models": list(self._models_cache.keys()),
            "cache_size": len(self._models_cache)
        }


# Global loader instance
model_loader = ModelLoader()
