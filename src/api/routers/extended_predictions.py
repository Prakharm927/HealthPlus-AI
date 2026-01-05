"""
Extended working prediction endpoints for all 7 diseases
"""
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

from src.models.mock_predictions import mock_engine
from src.monitoring.logger import logger

router = APIRouter(prefix="/api/predict", tags=["All Disease Predictions"])


# Liver Disease Request
class LiverRequest(BaseModel):
    age: int = Field(..., ge=1, le=120)
    total_bilirubin: float = Field(..., ge=0.1, le=20, description="Total bilirubin mg/dL")
    alkaline_phosphotase: int = Field(..., ge=20, le=400, description="ALP U/L")
    alamine_aminotransferase: int = Field(..., ge=5, le=400, description="ALT U/L")
    aspartate_aminotransferase: int = Field(..., ge=5, le=400, description="AST U/L")


#Breast Cancer Request
class BreastCancerRequest(BaseModel):
    texture_mean: float = Field(..., ge=5, le=40, description="Texture")  
    perimeter_mean: float = Field(..., ge=40, le=200, description="Perimeter")
    area_mean: float = Field(..., ge=100, le=2500, description="Area")
    concavity_mean: float = Field(..., ge=0, le=0.5, description="Concavity")


# Parkinson's Request
class ParkinsonsRequest(BaseModel):
    mdvp_jitter: float = Field(..., ge=0.001, le=0.05, description="Jitter")
    shimmer: float = Field(..., ge=0.01, le=0.3, description="Shimmer")
    nhr: float = Field(..., ge=0.001, le=0.2, description="NHR")
    hnr: float = Field(..., ge=5, le=40, description="HNR dB")


# Generic Result Model
class PredictionResult(BaseModel):
    success: bool = True
    prediction: str
    confidence: float
    recommendation: str
    color: str
    model_name: str
    model_version: str
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())


@router.post("/kidney", response_model=PredictionResult)
async def predict_kidney():
    """Kidney Disease Detection (CT Scan simulation)"""
    try:
        result = mock_engine.predict_kidney_disease()
        logger.info(f"Kidney prediction: {result['prediction']}")
        
        return PredictionResult(
            prediction=result['prediction'],
            confidence=result['confidence'],
            recommendation=result['recommendation'],
            color=result['color'],
            model_name=result['model_name'],
            model_version=result['model_version']
        )
    except Exception as e:
        logger.error(f"Kidney prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/liver", response_model=PredictionResult)
async def predict_liver(request: LiverRequest):
    """Liver Disease Screening"""
    try:
        result = mock_engine.predict_liver_disease(request.dict())
        logger.info(f"Liver prediction: {result['prediction']}")
        
        # Handle risk_factors field
        factors_str = ", ".join(result.get('risk_factors', []))
        
        return PredictionResult(
            prediction=result['prediction'],
            confidence=result['confidence'],
            recommendation=result['recommendation'] + f" | Factors: {factors_str}",
            color=result['color'],
            model_name=result['model_name'],
            model_version=result['model_version']
        )
    except Exception as e:
        logger.error(f"Liver prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/breast-cancer", response_model=PredictionResult)
async def predict_breast_cancer(request: BreastCancerRequest):
    """Breast Cancer Classification"""
    try:
        result = mock_engine.predict_breast_cancer(request.dict())
        logger.info(f"Breast cancer prediction: {result['prediction']}")
        
        return PredictionResult(
            prediction=result['prediction'],
            confidence=result['confidence'],
            recommendation=result['recommendation'],
            color=result['color'],
            model_name=result['model_name'],
            model_version=result['model_version']
        )
    except Exception as e:
        logger.error(f"Breast cancer prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/parkinsons", response_model=PredictionResult)
async def predict_parkinsons(request: ParkinsonsRequest):
    """Parkinson's Disease Detection"""
    try:
        result = mock_engine.predict_parkinsons(request.dict())
        logger.info(f"Parkinson's prediction: {result['prediction']}")
        
        # Handle indicators field
        indicators_str = ", ".join(result.get('indicators', []))
        
        return PredictionResult(
            prediction=result['prediction'],
            confidence=result['confidence'],
            recommendation=result['recommendation'] + f" | Factors: {indicators_str}",
            color=result['color'],
            model_name=result['model_name'],
            model_version=result['model_version']
        )
    except Exception as e:
        logger.error(f"Parkinson's prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/brain-tumor", response_model=PredictionResult)
async def predict_brain_tumor():
    """Brain Tumor Classification (MRI simulation)"""
    try:
        result = mock_engine.predict_brain_tumor()
        logger.info(f"Brain tumor prediction: {result['prediction']}")
        
        return PredictionResult(
            prediction=result['prediction'],
            confidence=result['confidence'],
            recommendation=result['recommendation'],
            color=result['color'],
            model_name=result['model_name'],
            model_version=result['model_version']  
        )
    except Exception as e:
        logger.error(f"Brain tumor prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
