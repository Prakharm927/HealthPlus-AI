"""
Data drift detection utilities
Compares incoming data distributions with reference statistics
"""

import json
import numpy as np
from typing import Dict, Optional, Tuple
from pathlib import Path
from datetime import datetime
from src.monitoring.logger import logger
from config.settings import get_settings


class DriftDetector:
    """
    Statistical drift detector for monitoring data distribution changes
    Uses simple mean and standard deviation comparison
    """
    
    def __init__(self, reference_stats_dir: str = "models/reference_stats"):
        self.reference_stats_dir = Path(reference_stats_dir)
        self.reference_stats_dir.mkdir(parents=True, exist_ok=True)
        self.settings = get_settings()
    
    def calculate_statistics(self, data: np.ndarray) -> Dict[str, float]:
        """
        Calculate distribution statistics
        
        Args:
            data: Input data array
        
        Returns:
            Dictionary of statistics
        """
        return {
            "mean": float(np.mean(data)),
            "std": float(np.std(data)),
            "min": float(np.min(data)),
            "max": float(np.max(data)),
            "median": float(np.median(data))
        }
    
    def save_reference_stats(self, model_name: str, data: np.ndarray):
        """
        Save reference statistics for a model
        
        Args:
            model_name: Name of the model
            data: Reference dataset
        """
        stats = self.calculate_statistics(data)
        stats["timestamp"] = datetime.utcnow().isoformat()
        stats["sample_size"] = int(len(data))
        
        stats_file = self.reference_stats_dir / f"{model_name}_stats.json"
        
        with open(stats_file, 'w') as f:
            json.dump(stats, f, indent=2)
        
        logger.info(f"Saved reference statistics for {model_name}")
    
    def load_reference_stats(self, model_name: str) -> Optional[Dict]:
        """
        Load reference statistics for a model
        
        Args:
            model_name: Name of the model
        
        Returns:
            Dictionary of reference statistics, or None if not found
        """
        stats_file = self.reference_stats_dir / f"{model_name}_stats.json"
        
        if not stats_file.exists():
            logger.warning(f"No reference statistics found for {model_name}")
            return None
        
        with open(stats_file, 'r') as f:
            return json.load(f)
    
    def detect_drift(
        self,
        model_name: str,
        current_data: np.ndarray,
        threshold: float = None
    ) -> Tuple[bool, Dict]:
        """
        Detect drift in current data compared to reference
        
        Args:
            model_name: Name of the model
            current_data: Current dataset
            threshold: Drift threshold (uses config default if not specified)
        
        Returns:
            Tuple of (drift_detected, drift_metrics)
        """
        threshold = threshold or self.settings.drift_threshold
        
        # Load reference statistics
        reference_stats = self.load_reference_stats(model_name)
        if reference_stats is None:
            logger.warning(f"Cannot detect drift for {model_name}: no reference stats")
            return False, {}
        
        # Calculate current statistics
        current_stats = self.calculate_statistics(current_data)
        
        # Calculate drift scores
        mean_diff = abs(current_stats["mean"] - reference_stats["mean"])
        std_diff = abs(current_stats["std"] - reference_stats["std"])
        
        # Normalize by reference values
        mean_drift = mean_diff / (abs(reference_stats["mean"]) + 1e-8)
        std_drift = std_diff / (reference_stats["std"] + 1e-8)
        
        # Overall drift score (simple average)
        overall_drift = (mean_drift + std_drift) / 2
        
        # Determine if drift detected
        drift_detected = overall_drift > threshold
        
        drift_metrics = {
            "overall_drift": float(overall_drift),
            "mean_drift": float(mean_drift),
            "std_drift": float(std_drift),
            "threshold": threshold,
            "drift_detected": drift_detected,
            "current_stats": current_stats,
            "reference_stats": reference_stats,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        if drift_detected:
            logger.warning(
                f"Data drift detected for {model_name}: {overall_drift:.3f} > {threshold}",
                extra={"model_name": model_name}
            )
        else:
            logger.info(
                f"No drift detected for {model_name}: {overall_drift:.3f} <= {threshold}",
                extra={"model_name": model_name}
            )
        
        return drift_detected, drift_metrics
    
    def update_reference_stats(self, model_name: str, new_data: np.ndarray):
        """
        Update reference statistics with new data (for retraining scenarios)
        
        Args:
            model_name: Name of the model
            new_data: New reference dataset
        """
        self.save_reference_stats(model_name, new_data)
        logger.info(f"Updated reference statistics for {model_name}")


# Global drift detector instance
drift_detector = DriftDetector()
