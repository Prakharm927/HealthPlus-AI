"""
Configuration management using Pydantic Settings
Environment-based configuration for production deployment
"""

from functools import lru_cache
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration"""
    
    # API Settings
    app_name: str = "OpenHealth AI Service"
    app_version: str = "1.0.0"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Model Settings
    model_version: str = "v1"
    models_dir: str = "models"
    confidence_threshold: float = 0.75
    
    # Monitoring Settings
    log_level: str = "INFO"
    monitoring_enabled: bool = True
    metrics_enabled: bool = True
    
    # External APIs
    google_api_key: Optional[str] = None
    
    # Data Pipeline Settings
    data_validation_enabled: bool = True
    drift_detection_enabled: bool = True
    drift_threshold: float = 0.3
    
    # Performance Settings
    max_workers: int = 4
    request_timeout: int = 30
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
