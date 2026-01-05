"""
Pydantic schemas for request/response validation
"""

from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field, confloat, conint
from datetime import datetime


# ============================================================================
# Health Check Schemas
# ============================================================================

class HealthCheckResponse(BaseModel):
    """Health check response"""
    status: str = Field(..., description="Service health status")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    version: str = Field(..., description="API version")


class ModelInfo(BaseModel):
    """Individual model information"""
    name: str
    version: str
    type: str
    loaded: bool
    confidence_threshold: float


class ModelInfoResponse(BaseModel):
    """Model information response"""
    models: List[ModelInfo]
    active_version: str
    total_models: int


# ============================================================================
# Generic Prediction Schemas
# ============================================================================

class PredictionResponse(BaseModel):
    """Generic prediction response"""
    prediction: str = Field(..., description="Prediction result")
    confidence: confloat(ge=0.0, le=1.0) = Field(..., description="Prediction confidence score")
    model_version: str = Field(..., description="Model version used")
    model_name: str = Field(..., description="Model name")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")
    fallback_used: bool = Field(default=False, description="Whether fallback logic was triggered")


# ============================================================================
# Brain Tumor Prediction
# ============================================================================

class BrainTumorRequest(BaseModel):
    """Brain tumor prediction request"""
    image_base64: str = Field(..., description="Base64 encoded image")
    
    class Config:
        json_schema_extra = {
            "example": {
                "image_base64": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
            }
        }


class BrainTumorResponse(PredictionResponse):
    """Brain tumor prediction response"""
    tumor_type: str = Field(..., description="Type of tumor detected")


# ============================================================================
# Heart Disease Prediction
# ============================================================================

class HeartDiseaseRequest(BaseModel):
    """Heart disease prediction request"""
    age: conint(ge=0, le=120) = Field(..., description="Age in years")
    sex: conint(ge=0, le=1) = Field(..., description="Sex (0=female, 1=male)")
    cp: conint(ge=0, le=3) = Field(..., description="Chest pain type (0-3)")
    trestbps: conint(ge=50, le=250) = Field(..., description="Resting blood pressure")
    chol: conint(ge=100, le=600) = Field(..., description="Serum cholesterol in mg/dl")
    fbs: conint(ge=0, le=1) = Field(..., description="Fasting blood sugar > 120 mg/dl")
    restecg: conint(ge=0, le=2) = Field(..., description="Resting ECG results")
    thalach: conint(ge=50, le=250) = Field(..., description="Maximum heart rate achieved")
    exang: conint(ge=0, le=1) = Field(..., description="Exercise induced angina")
    oldpeak: confloat(ge=0.0, le=10.0) = Field(..., description="ST depression")
    slope: conint(ge=0, le=2) = Field(..., description="Slope of peak exercise ST segment")
    ca: conint(ge=0, le=4) = Field(..., description="Number of major vessels")
    thal: conint(ge=0, le=3) = Field(..., description="Thalassemia")
    
    class Config:
        json_schema_extra = {
            "example": {
                "age": 63,
                "sex": 1,
                "cp": 3,
                "trestbps": 145,
                "chol": 233,
                "fbs": 1,
                "restecg": 0,
                "thalach": 150,
                "exang": 0,
                "oldpeak": 2.3,
                "slope": 0,
                "ca": 0,
                "thal": 1
            }
        }


# ============================================================================
# Diabetes Prediction
# ============================================================================

class DiabetesRequest(BaseModel):
    """Diabetes prediction request"""
    pregnancies: conint(ge=0, le=20) = Field(..., description="Number of pregnancies")
    glucose: conint(ge=0, le=300) = Field(..., description="Plasma glucose concentration")
    blood_pressure: conint(ge=0, le=200) = Field(..., description="Diastolic blood pressure (mm Hg)")
    skin_thickness: conint(ge=0, le=100) = Field(..., description="Triceps skin fold thickness (mm)")
    insulin: conint(ge=0, le=900) = Field(..., description="2-Hour serum insulin (mu U/ml)")
    bmi: confloat(ge=0.0, le=70.0) = Field(..., description="Body mass index")
    diabetes_pedigree_function: confloat(ge=0.0, le=3.0) = Field(..., description="Diabetes pedigree function")
    age: conint(ge=0, le=120) = Field(..., description="Age in years")
    
    class Config:
        json_schema_extra = {
            "example": {
                "pregnancies": 6,
                "glucose": 148,
                "blood_pressure": 72,
                "skin_thickness": 35,
                "insulin": 0,
                "bmi": 33.6,
                "diabetes_pedigree_function": 0.627,
                "age": 50
            }
        }


# ============================================================================
# Kidney Disease Prediction
# ============================================================================

class KidneyDiseaseRequest(BaseModel):
    """Kidney disease prediction request"""
    image_base64: str = Field(..., description="Base64 encoded CT scan image")


class KidneyDiseaseResponse(PredictionResponse):
    """Kidney disease prediction response"""
    condition: str = Field(..., description="Detected kidney condition")


# ============================================================================
# Liver Disease Prediction
# ============================================================================

class LiverDiseaseRequest(BaseModel):
    """Liver disease prediction request"""
    age: conint(ge=0, le=120) = Field(..., description="Age of the patient")
    gender: conint(ge=0, le=1) = Field(..., description="Gender (0=female, 1=male)")
    total_bilirubin: confloat(ge=0.0) = Field(..., description="Total Bilirubin")
    direct_bilirubin: confloat(ge=0.0) = Field(..., description="Direct Bilirubin")
    alkaline_phosphotase: confloat(ge=0.0) = Field(..., description="Alkaline Phosphotase")
    alamine_aminotransferase: confloat(ge=0.0) = Field(..., description="Alamine Aminotransferase")
    aspartate_aminotransferase: confloat(ge=0.0) = Field(..., description="Aspartate Aminotransferase")
    total_proteins: confloat(ge=0.0) = Field(..., description="Total Proteins")
    albumin: confloat(ge=0.0) = Field(..., description="Albumin")
    albumin_globulin_ratio: confloat(ge=0.0) = Field(..., description="Albumin and Globulin Ratio")


# ============================================================================
# Breast Cancer Prediction
# ============================================================================

class BreastCancerRequest(BaseModel):
    """Breast cancer prediction request"""
    texture_mean: confloat(ge=0.0) = Field(...)
    smoothness_mean: confloat(ge=0.0) = Field(...)
    compactness_mean: confloat(ge=0.0) = Field(...)
    concave_points_mean: confloat(ge=0.0) = Field(...)
    symmetry_mean: confloat(ge=0.0) = Field(...)
    fractal_dimension_mean: confloat(ge=0.0) = Field(...)
    texture_se: confloat(ge=0.0) = Field(...)
    area_se: confloat(ge=0.0) = Field(...)
    smoothness_se: confloat(ge=0.0) = Field(...)
    compactness_se: confloat(ge=0.0) = Field(...)
    concavity_se: confloat(ge=0.0) = Field(...)
    concave_points_se: confloat(ge=0.0) = Field(...)
    symmetry_se: confloat(ge=0.0) = Field(...)
    fractal_dimension_se: confloat(ge=0.0) = Field(...)
    texture_worst: confloat(ge=0.0) = Field(...)
    area_worst: confloat(ge=0.0) = Field(...)
    smoothness_worst: confloat(ge=0.0) = Field(...)
    compactness_worst: confloat(ge=0.0) = Field(...)
    concavity_worst: confloat(ge=0.0) = Field(...)
    concave_points_worst: confloat(ge=0.0) = Field(...)
    symmetry_worst: confloat(ge=0.0) = Field(...)
    fractal_dimension_worst: confloat(ge=0.0) = Field(...)


# ============================================================================
# Parkinsons Prediction
# ============================================================================

class ParkinsonsRequest(BaseModel):
    """Parkinson's disease prediction request"""
    mdvp_fo: confloat(ge=0.0) = Field(..., description="MDVP:Fo(Hz)")
    mdvp_fhi: confloat(ge=0.0) = Field(..., description="MDVP:Fhi(Hz)")
    mdvp_flo: confloat(ge=0.0) = Field(..., description="MDVP:Flo(Hz)")
    mdvp_jitter: confloat(ge=0.0) = Field(..., description="MDVP:Jitter(%)")
    rpde: confloat(ge=0.0) = Field(..., description="RPDE")
    dfa: confloat(ge=0.0) = Field(..., description="DFA")
    spread2: confloat() = Field(..., description="spread2")
    d2: confloat(ge=0.0) = Field(..., description="D2")


# ============================================================================
# Error Response
# ============================================================================

class ErrorResponse(BaseModel):
    """Error response schema"""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(default=None, description="Detailed error information")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    request_id: Optional[str] = Field(default=None)
