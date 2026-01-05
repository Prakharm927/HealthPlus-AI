"""
Simple working prediction endpoints using mock models
Fast, no dependencies, ready for demo
"""
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

# Import mock engine
from src.models.mock_predictions import mock_engine
from src.monitoring.logger import logger

router = APIRouter(prefix="/api/predict", tags=["Working Predictions"])


# Simple request/response models
class SimpleHeartRequest(BaseModel):
    age: int = Field(..., ge=1, le=120, description="Patient age")
    chol: int = Field(..., ge=100, le=400, description="Cholesterol level mg/dL")
    trestbps: int = Field(..., ge=80, le=200, description="Resting blood pressure mmHg")
    cp: int = Field(default=0, ge=0, le=3, description="Chest pain type (0-3)")
    fbs: int = Field(default=0, ge=0, le=1, description="Fasting blood sugar > 120 mg/dl")


class SimpleDiabetesRequest(BaseModel):
    glucose: float = Field(..., ge=50, le=250, description="Fasting glucose mg/dL")
    bmi: float = Field(..., ge=15, le=60, description="Body Mass Index")
    age: int = Field(..., ge=1, le=120, description="Patient age")
    blood_pressure: int = Field(default=80, ge=50, le=150, description="Blood pressure")


class PredictionResult(BaseModel):
    success: bool = True
    prediction: str
    confidence: float
    risk_score: Optional[float] = None
    probability: Optional[float] = None
    risk_factors: list
    recommendation: str
    color: str
    model_name: str
    model_version: str
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())


@router.post("/heart", response_model=PredictionResult, summary="Heart Disease Risk Calculator")
async def predict_heart_simple(request: SimpleHeartRequest):
    """
    ## Heart Disease Risk Assessment
    
    Input your health metrics to get instant risk assessment.
    
    **Example:**
    ```json
    {
        "age": 63,
        "chol": 233,
        "trestbps": 145,
        "cp": 3,
        "fbs": 1
    }
    ```
    
    **Returns:** Risk score, confidence, and medical recommendations
    """
    try:
        # Call mock prediction engine
        result = mock_engine.predict_heart_disease(request.dict())
        
        logger.info(f"Heart prediction: {result['prediction']} (confidence: {result['confidence']})")
        
        return PredictionResult(
            prediction=result['prediction'],
            confidence=result['confidence'],
            risk_score=result['risk_score'],
            risk_factors=result['risk_factors'],
            recommendation=result['recommendation'],
            color=result['color'],
            model_name=result['model_name'],
            model_version=result['model_version']
        )
        
    except Exception as e:
        logger.error(f"Heart prediction error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}"
        )


@router.post("/diabetes", response_model=PredictionResult, summary="Diabetes Risk Calculator")
async def predict_diabetes_simple(request: SimpleDiabetesRequest):
    """
    ## Diabetes Risk Assessment
    
    Check your diabetes risk with simple health metrics.
    
    **Example:**
    ```json
    {
        "glucose": 148,
        "bmi": 33.6,
        "age": 50,
        "blood_pressure": 72
    }
    ```
    
    **Returns:** Risk probability, factors, and health advice
    """
    try:
        result = mock_engine.predict_diabetes(request.dict())
        
        logger.info(f"Diabetes prediction: {result['prediction']} (probability: {result['probability']})")
        
        return PredictionResult(
            prediction=result['prediction'],
            confidence=result['confidence'],
            probability=result['probability'],
            risk_factors=result['risk_factors'],
            recommendation=result['recommendation'],
            color=result['color'],
            model_name=result['model_name'],
            model_version=result['model_version']
        )
        
    except Exception as e:
        logger.error(f"Diabetes prediction error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}"
        )


@router.get("/test", summary="Test API connectivity")
async def test_predictions():
    """Quick test endpoint to verify API is working"""
    return {
        "status": "healthy",
        "message": "Prediction API is working!",
        "available_endpoints": ["/api/predict/heart", "/api/predict/diabetes"],
        "timestamp": datetime.now().isoformat()
    }
