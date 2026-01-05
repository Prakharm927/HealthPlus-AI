"""
Prediction endpoints for all disease models
"""

# Standard library imports only - NO heavy ML imports at module level!
from fastapi import APIRouter, HTTPException, status
from datetime import datetime

from src.api.schemas import (
    BrainTumorRequest, BrainTumorResponse,
    HeartDiseaseRequest, PredictionResponse,
    DiabetesRequest, KidneyDiseaseRequest, KidneyDiseaseResponse,
    LiverDiseaseRequest, BreastCancerRequest, ParkinsonsRequest
)
from src.models.registry import model_registry
from src.monitoring.metrics import metrics_collector, LatencyTimer
from src.monitoring.logger import logger
from config.settings import get_settings

router = APIRouter(prefix="/predict", tags=["Predictions"])


# Lazy import function for heavy ML libraries
def get_ml_libraries():
    """Lazy import of ML libraries - only called when prediction is made"""
    try:
        import base64
        import io
        import numpy as np
        from PIL import Image
        return base64, io, np, Image
    except ImportError as e:
        logger.error(f"Failed to import ML libraries: {e}")
        raise HTTPException(
            status_code=500,
            detail="ML libraries not available. Please install: pip install numpy Pillow"
        )


def get_model_loader():
    """Lazy import of model loader"""
    try:
        from src.models.loader import model_loader
        return model_loader
    except Exception as e:
        logger.error(f"Failed to import model loader: {e}")
        raise HTTPException(status_code=500, detail="Model loader not available")


def check_confidence_and_fallback(
    prediction: str,
    confidence: float,
    model_name: str,
    threshold: float = None
) -> tuple:
    """
    Check confidence and trigger fallback if needed
    Returns (prediction, confidence, fallback_used)
    """
    settings = get_settings()
    threshold = threshold or settings.confidence_threshold
    
    # Record confidence
    metrics_collector.record_confidence(model_name, confidence, threshold)
    
    # Check if fallback needed
    if confidence < threshold:
        logger.warning(
            f"Low confidence prediction for {model_name}: {confidence:.3f} < {threshold}",
            extra={"model_name": model_name, "confidence": confidence}
        )
        
        # Return safe fallback
        fallback_prediction = "Uncertain - please consult healthcare professional"
        return fallback_prediction, confidence, True
    
    return prediction, confidence, False


@router.post(
    "/brain-tumor",
    response_model=BrainTumorResponse,
    status_code=status.HTTP_200_OK,
    summary="Predict brain tumor type from MRI image"
)
async def predict_brain_tumor(request: BrainTumorRequest):
    """
    Predicts brain tumor type from MRI scan
    
    - **Input**: Base64 encoded MRI image
    - **Output**: Tumor type (Glioma, Meningioma, Pituitary, or No Tumor) with confidence
    """
    model_name = "brain_tumor"
    
    try:
        # Lazy import ML libraries only when needed
        base64, io, np, Image = get_ml_libraries()
        model_loader = get_model_loader()
        
        # Decode image
        image_bytes = base64.b64decode(request.image_base64)
        img = Image.open(io.BytesIO(image_bytes))
        
        # Preprocess
        img = img.resize((299, 299))
        img_array = np.asarray(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0
        
        # Load model and predict with latency tracking
        with LatencyTimer(model_name) as timer:
            model = model_loader.get_model(model_name)
            predictions = model.predict(img_array)
        
        # Parse results
        class_labels = {
            0: 'Glioma Tumor',
            1: 'Meningioma Tumor',
            2: 'No Tumor',
            3: 'Pituitary Tumor'
        }
        
        predicted_class = int(np.argmax(predictions))
        confidence = float(np.max(predictions))
        prediction = class_labels[predicted_class]
        
        # Check confidence and apply fallback if needed
        prediction, confidence, fallback_used = check_confidence_and_fallback(
            prediction, confidence, model_name
        )
        
        # Record metrics
        metrics_collector.record_prediction(model_name, True)
        
        logger.info(
            f"Brain tumor prediction: {prediction}",
            extra={
                "model_name": model_name,
                "confidence": confidence,
                "latency_ms": timer.latency_ms
            }
        )
        
        return BrainTumorResponse(
            prediction=prediction,
            tumor_type=prediction,
            confidence=confidence,
            model_version=model_registry.get_active_version(model_name),
            model_name=model_name,
            fallback_used=fallback_used
        )
        
    except Exception as e:
        metrics_collector.record_prediction(model_name, False)
        logger.error(f"Brain tumor prediction failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}"
        )


@router.post(
    "/heart-disease",
    response_model=PredictionResponse,
    status_code=status.HTTP_200_OK,
    summary="Predict heart disease risk"
)
async def predict_heart_disease(request: HeartDiseaseRequest):
    """
    Predicts heart disease risk based on clinical parameters
    
    - **Input**: 13 clinical features (age, sex, blood pressure, cholesterol, etc.)
    - **Output**: Risk score with confidence
    """
    model_name = "heart"
    
    try:
        # Prepare input data
        features = np.array([[
            request.age, request.sex, request.cp, request.trestbps,
            request.chol, request.fbs, request.restecg, request.thalach,
            request.exang, request.oldpeak, request.slope, request.ca,
            request.thal
        ]])
        
        # Load model and predict
        with LatencyTimer(model_name) as timer:
            model = model_loader.get_model(model_name)
            prediction_proba = model.predict_proba(features)[0]
        
        # Parse results
        risk_score = float(prediction_proba[1])
        prediction = "High Risk" if risk_score > 0.5 else "Low Risk"
        
        # Check confidence and apply fallback
        prediction, confidence, fallback_used = check_confidence_and_fallback(
            prediction, risk_score, model_name
        )
        
        # Record metrics
        metrics_collector.record_prediction(model_name, True)
        
        logger.info(
            f"Heart disease prediction: {prediction}",
            extra={
                "model_name": model_name,
                "confidence": confidence,
                "latency_ms": timer.latency_ms
            }
        )
        
        return PredictionResponse(
            prediction=prediction,
            confidence=confidence,
            model_version=model_registry.get_active_version(model_name),
            model_name=model_name,
            fallback_used=fallback_used,
            metadata={"risk_score": risk_score}
        )
        
    except Exception as e:
        metrics_collector.record_prediction(model_name, False)
        logger.error(f"Heart disease prediction failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}"
        )


@router.post(
    "/diabetes",
    response_model=PredictionResponse,
    status_code=status.HTTP_200_OK,
    summary="Predict diabetes risk"
)
async def predict_diabetes(request: DiabetesRequest):
    """
    Predicts diabetes risk based on patient data
    
    - **Input**: Pregnancies, glucose, blood pressure, BMI, etc.
    - **Output**: Diabetes risk prediction with confidence
    """
    model_name = "diabetes"
    
    try:
        # Prepare input data
        features = np.array([[
            request.pregnancies, request.glucose, request.blood_pressure,
            request.skin_thickness, request.insulin, request.bmi,
            request.diabetes_pedigree_function, request.age
        ]])
        
        # Load model and predict
        with LatencyTimer(model_name) as timer:
            model = model_loader.get_model(model_name)
            prediction_proba = model.predict_proba(features)[0]
        
        # Parse results
        diabetes_prob = float(prediction_proba[1])
        prediction = "Diabetic" if diabetes_prob > 0.5 else "Non-Diabetic"
        
        # Check confidence and apply fallback
        prediction, confidence, fallback_used = check_confidence_and_fallback(
            prediction, diabetes_prob, model_name
        )
        
        # Record metrics
        metrics_collector.record_prediction(model_name, True)
        
        logger.info(
            f"Diabetes prediction: {prediction}",
            extra={
                "model_name": model_name,
                "confidence": confidence,
                "latency_ms": timer.latency_ms
            }
        )
        
        return PredictionResponse(
            prediction=prediction,
            confidence=confidence,
            model_version=model_registry.get_active_version(model_name),
            model_name=model_name,
            fallback_used=fallback_used,
            metadata={"diabetes_probability": diabetes_prob}
        )
        
    except Exception as e:
        metrics_collector.record_prediction(model_name, False)
        logger.error(f"Diabetes prediction failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}"
        )


@router.post(
    "/kidney-disease",
    response_model=KidneyDiseaseResponse,
    status_code=status.HTTP_200_OK,
    summary="Predict kidney condition from CT scan"
)
async def predict_kidney_disease(request: KidneyDiseaseRequest):
    """
    Predicts kidney condition from CT scan image
    
    - **Input**: Base64 encoded CT scan image
    - **Output**: Condition (Cyst, Normal, Stone, or Tumor) with confidence
    """
    model_name = "kidney"
    
    try:
        # Decode and preprocess image
        image_bytes = base64.b64decode(request.image_base64)
        img = Image.open(io.BytesIO(image_bytes))
        img = img.resize((150, 150))
        img_array = np.asarray(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        
        # Load model and predict
        with LatencyTimer(model_name) as timer:
            model = model_loader.get_model(model_name)
            predictions = model.predict(img_array)
        
        # Parse results
        class_labels = {0: 'Cyst', 1: 'Normal', 2: 'Stone', 3: 'Tumor'}
        predicted_class = int(np.argmax(predictions))
        confidence = float(np.max(predictions))
        prediction = class_labels[predicted_class]
        
        # Check confidence and apply fallback
        prediction, confidence, fallback_used = check_confidence_and_fallback(
            prediction, confidence, model_name
        )
        
        # Record metrics
        metrics_collector.record_prediction(model_name, True)
        
        logger.info(
            f"Kidney disease prediction: {prediction}",
            extra={
                "model_name": model_name,
                "confidence": confidence,
                "latency_ms": timer.latency_ms
            }
        )
        
        return KidneyDiseaseResponse(
            prediction=prediction,
            condition=prediction,
            confidence=confidence,
            model_version=model_registry.get_active_version(model_name),
            model_name=model_name,
            fallback_used=fallback_used
        )
        
    except Exception as e:
        metrics_collector.record_prediction(model_name, False)
        logger.error(f"Kidney disease prediction failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}"
        )


@router.post(
    "/liver-disease",
    response_model=PredictionResponse,
    status_code=status.HTTP_200_OK,
    summary="Predict liver disease"
)
async def predict_liver_disease(request: LiverDiseaseRequest):
    """
    Predicts liver disease based on lab results
    
    - **Input**: Age, gender, bilirubin levels, enzyme levels, proteins, etc.
    - **Output**: Liver disease prediction with confidence
    """
    model_name = "liver"
    
    try:
        # Prepare input data
        features = np.array([[
            request.age, request.gender, request.total_bilirubin,
            request.direct_bilirubin, request.alkaline_phosphotase,
            request.alamine_aminotransferase, request.aspartate_aminotransferase,
            request.total_proteins, request.albumin, request.albumin_globulin_ratio
        ]])
        
        # Load model and predict
        with LatencyTimer(model_name) as timer:
            model = model_loader.get_model(model_name)
            prediction_proba = model.predict_proba(features)[0]
        
        # Parse results
        disease_prob = float(prediction_proba[1])
        prediction = "Positive" if disease_prob > 0.5 else "Negative"
        
        # Check confidence and apply fallback
        prediction, confidence, fallback_used = check_confidence_and_fallback(
            prediction, disease_prob, model_name
        )
        
        # Record metrics
        metrics_collector.record_prediction(model_name, True)
        
        logger.info(
            f"Liver disease prediction: {prediction}",
            extra={
                "model_name": model_name,
                "confidence": confidence,
                "latency_ms": timer.latency_ms
            }
        )
        
        return PredictionResponse(
            prediction=prediction,
            confidence=confidence,
            model_version=model_registry.get_active_version(model_name),
            model_name=model_name,
            fallback_used=fallback_used,
            metadata={"disease_probability": disease_prob}
        )
        
    except Exception as e:
        metrics_collector.record_prediction(model_name, False)
        logger.error(f"Liver disease prediction failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}"
        )


@router.post(
    "/breast-cancer",
    response_model=PredictionResponse,
    status_code=status.HTTP_200_OK,
    summary="Predict breast cancer"
)
async def predict_breast_cancer(request: BreastCancerRequest):
    """
    Predicts breast cancer based on cell nucleus features
    
    - **Input**: 22 features from cell nucleus measurements
    - **Output**: Cancer prediction with confidence
    """
    model_name = "breast_cancer"
    
    try:
        # Prepare input data
        features = np.array([[
            request.texture_mean, request.smoothness_mean, request.compactness_mean,
            request.concave_points_mean, request.symmetry_mean, request.fractal_dimension_mean,
            request.texture_se, request.area_se, request.smoothness_se,
            request.compactness_se, request.concavity_se, request.concave_points_se,
            request.symmetry_se, request.fractal_dimension_se, request.texture_worst,
            request.area_worst, request.smoothness_worst, request.compactness_worst,
            request.concavity_worst, request.concave_points_worst, request.symmetry_worst,
            request.fractal_dimension_worst
        ]])
        
        # Load model and predict
        with LatencyTimer(model_name) as timer:
            model = model_loader.get_model(model_name)
            prediction_result = model.predict(features)[0]
        
        # Parse results (assuming binary prediction with confidence)
        confidence = float(abs(prediction_result))
        prediction = "Malignant" if prediction_result > 0 else "Benign"
        
        # Normalize confidence to [0, 1]
        if confidence > 1:
            confidence = min(confidence / 10, 1.0)
        
        # Check confidence and apply fallback
        prediction, confidence, fallback_used = check_confidence_and_fallback(
            prediction, confidence, model_name
        )
        
        # Record metrics
        metrics_collector.record_prediction(model_name, True)
        
        logger.info(
            f"Breast cancer prediction: {prediction}",
            extra={
                "model_name": model_name,
                "confidence": confidence,
                "latency_ms": timer.latency_ms
            }
        )
        
        return PredictionResponse(
            prediction=prediction,
            confidence=confidence,
            model_version=model_registry.get_active_version(model_name),
            model_name=model_name,
            fallback_used=fallback_used
        )
        
    except Exception as e:
        metrics_collector.record_prediction(model_name, False)
        logger.error(f"Breast cancer prediction failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}"
        )


@router.post(
    "/parkinsons",
    response_model=PredictionResponse,
    status_code=status.HTTP_200_OK,
    summary="Predict Parkinson's disease"
)
async def predict_parkinsons(request: ParkinsonsRequest):
    """
    Predicts Parkinson's disease based on voice measurements
    
    - **Input**: Voice features (jitter, shimmer, RPDE, DFA, etc.)
    - **Output**: Parkinson's prediction with confidence
    """
    model_name = "parkinsons"
    
    try:
        # Prepare input data
        features = np.array([[
            request.mdvp_fo, request.mdvp_fhi, request.mdvp_flo,
            request.mdvp_jitter, request.rpde, request.dfa,
            request.spread2, request.d2
        ]])
        
        # Load model and predict
        with LatencyTimer(model_name) as timer:
            model = model_loader.get_model(model_name)
            prediction_result = model.predict(features)[0]
        
        # Parse results
        confidence = float(abs(prediction_result))
        prediction = "Parkinson's Detected" if prediction_result > 0 else "No Parkinson's"
        
        # Normalize confidence
        if confidence > 1:
            confidence = min(confidence / 10, 1.0)
        
        # Check confidence and apply fallback
        prediction, confidence, fallback_used = check_confidence_and_fallback(
            prediction, confidence, model_name
        )
        
        # Record metrics
        metrics_collector.record_prediction(model_name, True)
        
        logger.info(
            f"Parkinsons prediction: {prediction}",
            extra={
                "model_name": model_name,
                "confidence": confidence,
                "latency_ms": timer.latency_ms
            }
        )
        
        return PredictionResponse(
            prediction=prediction,
            confidence=confidence,
            model_version=model_registry.get_active_version(model_name),
            model_name=model_name,
            fallback_used=fallback_used
        )
        
    except Exception as e:
        metrics_collector.record_prediction(model_name, False)
        logger.error(f"Parkinsons prediction failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}"
        )
