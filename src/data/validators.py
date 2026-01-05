"""
Data validation utilities
Input validation and quality checks
"""

import numpy as np
from typing import Dict, List, Any
from pydantic import BaseModel, ValidationError
from src.monitoring.logger import logger


class DataValidator:
    """
    Data quality validator for input validation
    Checks for missing values, outliers, and data quality issues
    """
    
    @staticmethod
    def check_missing_values(data: np.ndarray) -> Dict[str, Any]:
        """
        Check for missing or NaN values in the data
        
        Args:
            data: Input data array
        
        Returns:
            Validation result dictionary
        """
        missing_count = np.isnan(data).sum()
        total_values = data.size
        missing_percentage = (missing_count / total_values) * 100
        
        is_valid = missing_count == 0
        
        return {
            "check": "missing_values",
            "is_valid": is_valid,
            "missing_count": int(missing_count),
            "  total_values": int(total_values),
            "missing_percentage": float(missing_percentage)
        }
    
    @staticmethod
    def check_outliers(data: np.ndarray, threshold: float = 3.0) -> Dict[str, Any]:
        """
        Check for outliers using z-score method
        
        Args:
            data: Input data array
            threshold: Z-score threshold for outliers
        
        Returns:
            Validation result dictionary
        """
        mean = np.mean(data)
        std = np.std(data)
        
        if std == 0:
            return {
                "check": "outliers",
                "is_valid": True,
                "outlier_count": 0,
                "outlier_percentage": 0.0
            }
        
        z_scores = np.abs((data - mean) / std)
        outlier_count = np.sum(z_scores > threshold)
        total_values = data.size
        outlier_percentage = (outlier_count / total_values) * 100
        
        # Consider valid if less than 5% outliers
        is_valid = outlier_percentage < 5.0
        
        return {
            "check": "outliers",
            "is_valid": is_valid,
            "outlier_count": int(outlier_count),
            "total_values": int(total_values),
            "outlier_percentage": float(outlier_percentage),
            "threshold": threshold
        }
    
    @staticmethod
    def check_value_ranges(
        data: np.ndarray,
        expected_min: float = None,
        expected_max: float = None
    ) -> Dict[str, Any]:
        """
        Check if values are within expected ranges
        
        Args:
            data: Input data array
            expected_min: Expected minimum value
            expected_max: Expected maximum value
        
        Returns:
            Validation result dictionary
        """
        actual_min = float(np.min(data))
        actual_max = float(np.max(data))
        
        is_valid = True
        violations = []
        
        if expected_min is not None and actual_min < expected_min:
            is_valid = False
            violations.append(f"Minimum value {actual_min} < expected {expected_min}")
        
        if expected_max is not None and actual_max > expected_max:
            is_valid = False
            violations.append(f"Maximum value {actual_max} > expected {expected_max}")
        
        return {
            "check": "value_ranges",
            "is_valid": is_valid,
            "actual_min": actual_min,
            "actual_max": actual_max,
            "expected_min": expected_min,
            "expected_max": expected_max,
            "violations": violations
        }
    
    @classmethod
    def validate_input_data(
        cls,
        data: np.ndarray,
        model_name: str = None,
        check_outliers: bool = True,
        expected_min: float = None,
        expected_max: float = None
    ) -> Dict[str, Any]:
        """
        Perform comprehensive data validation
        
        Args:
            data: Input data array
            model_name: Name of the model (for logging)
            check_outliers: Whether to check for outliers
            expected_min: Expected minimum value
            expected_max: Expected maximum value
        
        Returns:
            Validation results dictionary
        """
        results = {
            "model_name": model_name,
            "checks": [],
            "is_valid": True
        }
        
        # Check missing values
        missing_check = cls.check_missing_values(data)
        results["checks"].append(missing_check)
        if not missing_check["is_valid"]:
            results["is_valid"] = False
        
        # Check outliers if requested
        if check_outliers:
            outlier_check = cls.check_outliers(data)
            results["checks"].append(outlier_check)
            if not outlier_check["is_valid"]:
                results["is_valid"] = False
                logger.warning(
                    f"Outliers detected: {outlier_check['outlier_percentage']:.2f}%",
                    extra={"model_name": model_name}
                )
        
        # Check value ranges if specified
        if expected_min is not None or expected_max is not None:
            range_check = cls.check_value_ranges(data, expected_min, expected_max)
            results["checks"].append(range_check)
            if not range_check["is_valid"]:
                results["is_valid"] = False
                logger.warning(
                    f"Value range violations: {range_check['violations']}",
                    extra={"model_name": model_name}
                )
        
        # Log validation result
        if not results["is_valid"]:
            logger.warning(
                f"Data validation failed for {model_name}",
                extra={"model_name": model_name}
            )
        
        return results


# Global validator instance
data_validator = DataValidator()
