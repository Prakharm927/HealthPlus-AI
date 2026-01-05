"""
Model version registry and management
Handles model versioning, rollback, and metadata tracking
"""

import json
import os
from pathlib import Path
from typing import Dict, Optional, List
from datetime import datetime
from config.settings import get_settings
from src.monitoring.logger import logger


class ModelRegistry:
    """
    Model version registry for tracking and managing model versions
    Supports version switching, rollback, and metadata management
    """
    
    def __init__(self, models_dir: str = None):
        settings = get_settings()
        self.models_dir = Path(models_dir or settings.models_dir)
        self.active_versions_file = self.models_dir / "active_versions.json"
        self._active_versions: Dict[str, str] = {}
        self._model_metadata: Dict[str, Dict] = {}
        self._load_active_versions()
    
    def _load_active_versions(self):
        """Load active version configuration"""
        if self.active_versions_file.exists():
            try:
                with open(self.active_versions_file, 'r') as f:
                    self._active_versions = json.load(f)
                logger.info(f"Loaded active versions: {self._active_versions}")
            except Exception as e:
                logger.error(f"Failed to load active versions: {e}")
                self._active_versions = {}
        else:
            # Initialize with v1 defaults
            self._active_versions = {
                "brain_tumor": "v1",
                "kidney": "v1",
                "liver": "v1",
                "heart": "v1",
                "diabetes": "v1",
                "breast_cancer": "v1",
                "parkinsons": "v1"
            }
            self._save_active_versions()
    
    def _save_active_versions(self):
        """Save active version configuration"""
        try:
            self.models_dir.mkdir(parents=True, exist_ok=True)
            with open(self.active_versions_file, 'w') as f:
                json.dump(self._active_versions, f, indent=2)
            logger.info(f"Saved active versions: {self._active_versions}")
        except Exception as e:
            logger.error(f"Failed to save active versions: {e}")
    
    def get_active_version(self, model_name: str) -> str:
        """Get active version for a model"""
        # Check environment variable override
        settings = get_settings()
        env_version = settings.model_version
        
        # If env variable is set and not default, use it
        if env_version and env_version != "v1":
            return env_version
        
        # Otherwise use registry
        return self._active_versions.get(model_name, "v1")
    
    def set_active_version(self, model_name: str, version: str):
        """Set active version for a model"""
        old_version = self._active_versions.get(model_name)
        self._active_versions[model_name] = version
        self._save_active_versions()
        
        logger.info(
            f"Version switch for {model_name}: {old_version} -> {version}",
            extra={"model_name": model_name}
        )
    
    def get_model_path(self, model_name: str, version: str = None) -> Path:
        """Get path to model file"""
        if version is None:
            version = self.get_active_version(model_name)
        
        # Determine file extension based on model type
        extension_map = {
            "brain_tumor": ".h5",
            "kidney": ".h5",
            "liver": ".pkl",
            "heart": ".pkl",
            "diabetes": ".pkl",
            "breast_cancer": ".pkl",
            "parkinsons": ".pkl"
        }
        
        extension = extension_map.get(model_name, ".pkl")
        model_path = self.models_dir / version / f"{model_name}{extension}"
        
        return model_path
    
    def get_metadata_path(self, model_name: str, version: str = None) -> Path:
        """Get path to model metadata file"""
        if version is None:
            version = self.get_active_version(model_name)
        
        return self.models_dir / version / f"{model_name}_metadata.json"
    
    def load_metadata(self, model_name: str, version: str = None) -> Dict:
        """Load model metadata"""
        metadata_path = self.get_metadata_path(model_name, version)
        
        if metadata_path.exists():
            try:
                with open(metadata_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Failed to load metadata for {model_name}: {e}")
        
        # Return default metadata if file doesn't exist
        return {
            "name": model_name,
            "version": version or self.get_active_version(model_name),
            "created_at": datetime.utcnow().isoformat(),
            "model_type": "unknown",
            "metrics": {}
        }
    
    def save_metadata(self, model_name: str, metadata: Dict, version: str = None):
        """Save model metadata"""
        metadata_path = self.get_metadata_path(model_name, version)
        metadata_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            logger.info(f"Saved metadata for {model_name}")
        except Exception as e:
            logger.error(f"Failed to save metadata for {model_name}: {e}")
    
    def get_available_versions(self, model_name: str) -> List[str]:
        """Get all available versions for a model"""
        versions = []
        
        if not self.models_dir.exists():
            return versions
        
        for version_dir in self.models_dir.iterdir():
            if version_dir.is_dir() and version_dir.name.startswith('v'):
                model_path = self.get_model_path(model_name, version_dir.name)
                if model_path.exists():
                    versions.append(version_dir.name)
        
        return sorted(versions)
    
    def rollback(self, model_name: str) -> Optional[str]:
        """
        Rollback to previous version of a model
        Returns the new active version, or None if rollback failed
        """
        available_versions = self.get_available_versions(model_name)
        current_version = self.get_active_version(model_name)
        
        if len(available_versions) < 2:
            logger.warning(f"Cannot rollback {model_name}: insufficient versions")
            return None
        
        # Find current version index
        try:
            current_idx = available_versions.index(current_version)
        except ValueError:
            logger.error(f"Current version {current_version} not found for {model_name}")
            return None
        
        # Get previous version
        if current_idx > 0:
            previous_version = available_versions[current_idx - 1]
        else:
            # Already on oldest version, wrap to newest
            previous_version = available_versions[-1]
        
        self.set_active_version(model_name, previous_version)
        logger.info(f"Rolled back {model_name} from {current_version} to {previous_version}")
        
        return previous_version
    
    def list_all_models(self) -> List[Dict]:
        """List all registered models with their metadata"""
        models = []
        
        for model_name in self._active_versions.keys():
            version = self.get_active_version(model_name)
            metadata = self.load_metadata(model_name, version)
            model_path = self.get_model_path(model_name, version)
            
            models.append({
                "name": model_name,
                "active_version": version,
                "available_versions": self.get_available_versions(model_name),
                "loaded": model_path.exists(),
                "metadata": metadata
            })
        
        return models


# Global registry instance
model_registry = ModelRegistry()
