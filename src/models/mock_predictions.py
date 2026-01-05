"""
Mock Prediction Engine
Smart rule-based predictions for demo/testing
Can be replaced with real ML models later
"""
from typing import Dict, Any, List
import random


class MockPredictionEngine:
    """Intelligent mock predictions based on medical logic"""
    
    @staticmethod
    def predict_heart_disease(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enhanced heart disease risk prediction based on clinical guidelines
        Uses improved risk scoring similar to Framingham/ACC-AHA models
        
        Factors weighted by medical importance:
        - age: Progressive risk increase
        - cholesterol: LDL threshold-based
        - blood pressure: Stage-based classification
        - chest pain: Symptom severity indicator
        - fasting blood sugar: Diabetes marker
        """
        age = int(data.get('age', 50))
        chol = int(data.get('chol', 200))
        trestbps = int(data.get('trestbps', 120))
        cp = int(data.get('cp', 0))
        fbs = int(data.get('fbs', 0))
        
        # Improved risk scoring algorithm
        risk_score = 0.0
        risk_factors = []
        severity_multiplier = 1.0
        
        # Age (progressive risk - most important factor)
        if age >= 65:
            risk_score += 0.35
            severity_multiplier *= 1.3
            risk_factors.append(f"Advanced age ({age}) - significantly elevated risk")
        elif age >= 55:
            risk_score += 0.25
            severity_multiplier *= 1.15
            risk_factors.append(f"Age ({age}) - moderately elevated risk")
        elif age >= 45:
            risk_score += 0.12
            risk_factors.append(f"Age ({age}) - mild risk elevation")
        
        # Cholesterol (LDL-based thresholds)
        if chol >= 280:
            risk_score += 0.30
            severity_multiplier *= 1.25
            risk_factors.append(f"Very high cholesterol ({chol} mg/dL) - requires medication")
        elif chol >= 240:
            risk_score += 0.22
            severity_multiplier *= 1.15
            risk_factors.append(f"High cholesterol ({chol} mg/dL) - medical intervention needed")
        elif chol >= 200:
            risk_score += 0.10
            risk_factors.append(f"Borderline high cholesterol ({chol} mg/dL)")
        elif chol < 170:
            risk_score -= 0.05  # Protective factor
        
        # Blood Pressure (Stage-based)
        if trestbps >= 160:
            risk_score += 0.28
            severity_multiplier *= 1.2
            risk_factors.append(f"Stage 2 hypertension ({trestbps} mmHg) - urgent treatment")
        elif trestbps >= 140:
            risk_score += 0.18
            severity_multiplier *= 1.1
            risk_factors.append(f"Stage 1 hypertension ({trestbps} mmHg)")
        elif trestbps >= 130:
            risk_score += 0.08
            risk_factors.append(f"Elevated blood pressure ({trestbps} mmHg)")
        elif trestbps < 120:
            risk_score -= 0.03  # Optimal BP
        
        # Chest Pain (Strong symptom indicator)
        if cp == 3:  # Asymptomatic (paradoxically worse in heart disease)
            risk_score += 0.18
            severity_multiplier *= 1.15
            risk_factors.append("Atypical chest pain pattern - requires investigation")
        elif cp == 2:
            risk_score += 0.12
            risk_factors.append("Non-anginal chest pain detected")
        elif cp == 1:
            risk_score += 0.08
            risk_factors.append("Atypical angina symptoms")
        
        # Fasting Blood Sugar (Diabetes indicator)
        if fbs == 1:
            risk_score += 0.18
            severity_multiplier *= 1.12
            risk_factors.append("Elevated fasting blood sugar - diabetes concern")
        
        # Apply severity multiplier
        risk_score = min(risk_score * severity_multiplier, 1.0)
        
        # Enhanced risk classification
        if risk_score >= 0.75:
            prediction = "Critical Risk"
            recommendation = "⚠️ URGENT: Immediate cardiology consultation required. Schedule ECG and stress test."
            color = "red"
        elif risk_score >= 0.60:
            prediction = "High Risk"
            recommendation = "Consult cardiologist within 1 week. Lifestyle modifications and medication likely needed."
            color = "red"
        elif risk_score >= 0.40:
            prediction = "Moderate Risk"
            recommendation = "Schedule checkup with healthcare provider. Start lifestyle changes (diet, exercise)."
            color = "orange"
        elif risk_score >= 0.20:
            prediction = "Low-Moderate Risk"
            recommendation = "Monitor regularly. Maintain healthy lifestyle and annual checkups."
            color = "orange"
        else:
            prediction = "Low Risk"
            recommendation = "Continue healthy lifestyle. Regular checkups recommended."
            color = "green"
        
        # Confidence based on data quality and risk extremity
        confidence = 0.78 + (abs(risk_score - 0.5) * 0.35)
        confidence = min(confidence, 0.98)
        
        # Add protective factors if low risk
        if not risk_factors:
            risk_factors.append("No major risk factors identified")
            risk_factors.append("Blood pressure within healthy range")
            risk_factors.append("Cholesterol levels acceptable")
        
        return {
            "prediction": prediction,
            "risk_score": round(risk_score, 3),
            "confidence": round(confidence, 3),
            "risk_factors": risk_factors,
            "recommendation": recommendation,
            "color": color,
            "model_name": "heart_disease",
            "model_version": "v1.1_enhanced"
        }
    
    @staticmethod
    def predict_diabetes(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enhanced diabetes risk prediction based on ADA guidelines
        Uses HbA1c thresholds and metabolic syndrome criteria
        
        Factors weighted by diagnostic importance:
        - glucose: Fasting plasma glucose (FPG) - primary diagnostic
        - bmi: Obesity indicator - major risk factor
        - age: Progressive risk
        - blood_pressure: Metabolic syndrome component
        """
        glucose = float(data.get('glucose', 100))
        bmi = float(data.get('bmi', 25))
        age = int(data.get('age', 40))
        bp = int(data.get('blood_pressure', 80))
        
        probability = 0.0
        factors = []
        severity_multiplier = 1.0
        
        # Glucose (ADA diagnostic criteria - most critical)
        if glucose >= 126:
            # Definitive diabetes threshold (fasting)
            probability += 0.55
            severity_multiplier *= 1.4
            factors.append(f"🔴 Glucose {glucose} mg/dL meets diabetes diagnostic criteria (≥126)")
        elif glucose >= 115:
            # High pre-diabetic
            probability += 0.35
            severity_multiplier *= 1.25
            factors.append(f"🟠 Glucose {glucose} mg/dL - high pre-diabetic range")
        elif glucose >= 100:
            # IFG (Impaired Fasting Glucose)
            probability += 0.22
            severity_multiplier *= 1.1
            factors.append(f"⚠️  Glucose {glucose} mg/dL - impaired fasting glucose (IFG)")
        elif glucose >= 90:
            probability += 0.08
            factors.append(f"Glucose {glucose} mg/dL - acceptable but monitor")
        else:
            probability -= 0.05  # Protective
        
        # BMI (Strong independent risk factor)
        if bmi >= 35:
            # Class II obesity
            probability += 0.25
            severity_multiplier *= 1.3
            factors.append(f"Severe obesity (BMI {bmi:.1f}) - very high diabetes risk")
        elif bmi >= 30:
            # Obese
            probability += 0.18
            severity_multiplier *= 1.15
            factors.append(f"Obesity (BMI {bmi:.1f}) - increased diabetes risk")
        elif bmi >= 27:
            probability += 0.12
            factors.append(f"Overweight (BMI {bmi:.1f}) - moderate risk factor")
        elif bmi >= 25:
            probability += 0.06
            factors.append(f"Overweight (BMI {bmi:.1f}) - mild risk")
        elif bmi < 23:
            probability -= 0.03  # Healthy weight protective
        
        # Age (Risk increases with age, especially >45)
        if age >= 65:
            probability += 0.15
            severity_multiplier *= 1.15
            factors.append(f"Age {age} - significantly increased diabetes prevalence")
        elif age >= 55:
            probability += 0.11
            factors.append(f"Age {age} - elevated diabetes risk")
        elif age >= 45:
            probability += 0.07
            factors.append(f"Age {age} - increased diabetes screening recommended")
        
        # Blood Pressure (Metabolic syndrome component)
        if bp >= 95:
            probability += 0.12
            severity_multiplier *= 1.08
            factors.append(f"Elevated BP ({bp} mmHg) - metabolic syndrome indicator")
        elif bp >= 85:
            probability += 0.06
            factors.append(f"Borderline BP ({bp} mmHg) - watch metabolic health")
        
        # Apply severity multiplier
        probability = min(probability * severity_multiplier, 1.0)
        
        # Enhanced classification with specific guidance
        if probability >= 0.70:
            prediction = "Diabetes Highly Likely"
            recommendation = "🔴 URGENT: See doctor immediately for HbA1c test and diabetes management. Start blood sugar monitoring."
            color = "red"
        elif probability >= 0.50:
            prediction = "High Risk - Probable Diabetes"
            recommendation = "Schedule urgent appointment for fasting glucose and HbA1c testing. Likely requires medication."
            color = "red"
        elif probability >= 0.35:
            prediction = "Pre-Diabetic Range"
            recommendation = "See doctor within 2 weeks. Start lifestyle changes: lose 5-7% body weight, exercise 150min/week."
            color = "orange"
        elif probability >= 0.20:
            prediction = "Moderate Risk"
            recommendation = "Annual screening recommended. Focus on weight management and physical activity."
            color = "orange"
        else:
            prediction = "Low Risk"
            recommendation = "Continue healthy habits. Screen every 3 years if no risk factors."
            color = "green"
        
        # High confidence for glucose-based diagnoses
        confidence = 0.82 + (abs(probability - 0.5) * 0.28)
        confidence = min(confidence, 0.97)
        
        # Add protective factors messaging
        if not factors:
            factors.append("No major risk factors identified")
            factors.append("Glucose within healthy range")
            factors.append("BMI within optimal range")
        
        # BMI category
        bmi_category = (
            "Underweight" if bmi < 18.5 else
            "Normal" if bmi < 25 else
            "Overweight" if bmi < 30 else
            "Obese Class I" if bmi < 35 else
            "Obese Class II+"
        )
        
        return {
            "prediction": prediction,
            "probability": round(probability, 3),
            "confidence": round(confidence, 3),
            "risk_factors": factors,
            "recommendation": recommendation,
            "color": color,
            "model_name": "diabetes",
            "model_version": "v1.1_ada_enhanced",
            "glucose_level": glucose,
            "bmi_category": bmi_category
        }
    
    @staticmethod
    def predict_brain_tumor(image_data: bytes = None) -> Dict[str, Any]:
        """
        Brain tumor classification (mock - image analysis)
        In real implementation, would use CNN model
        """
        # Mock classification
        tumor_types = ["No Tumor", "Glioma", "Meningioma", "Pituitary"]
        weights = [0.4, 0.3, 0.2, 0.1]  # Probability distribution
        
        prediction = random.choices(tumor_types, weights=weights)[0]
        
        if prediction == "No Tumor":
            confidence = random.uniform(0.85, 0.95)
            recommendation = "No tumor detected. Continue regular monitoring."
            color = "green"
        else:
            confidence = random.uniform(0.75, 0.92)
            recommendation = f"{prediction} detected. Immediate consultation with neurologist required."
            color = "red"
        
        return {
            "prediction": prediction,
            "confidence": round(confidence, 2),
            "tumor_type": prediction,
            "recommendation": recommendation,
            "color": color,
            "model_name": "brain_tumor",
            "model_version": "v1_mock",
            "scan_quality": "Good"
        }
    
    @staticmethod
    def predict_kidney_disease(data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Kidney disease detection (simplified - mock for CT scan analysis)
        In real implementation would analyze CT scan images
        """
        # For demo, use simple probability
        conditions = [
            {"name": "Normal", "prob": 0.50, "color": "green", "rec": "No abnormalities detected. Continue regular health checkups."},
            {"name": "Kidney Cyst", "prob": 0.25, "color": "orange", "rec": "Benign cyst detected. Monitor with periodic ultrasounds. Usually no treatment needed."},
            {"name": "Kidney Stone", "prob": 0.15, "color": "orange", "rec": "Kidney stone detected. Increase water intake (2-3L/day). Consult urologist if symptomatic."},
            {"name": "Kidney Tumor", "prob": 0.10, "color": "red", "rec": "⚠️ Tumor detected. URGENT: Immediate urologist consultation and further imaging required."}
        ]
        
        # Weighted random selection
        result = random.choices(conditions, weights=[c["prob"] for c in conditions])[0]
        confidence = random.uniform(0.82, 0.94) if result["name"] == "Normal" else random.uniform(0.76, 0.89)
        
        return {
            "prediction": result["name"],
            "condition": result["name"],
            "confidence": round(confidence, 3),
            "recommendation": result["rec"],
            "color": result["color"],
            "model_name": "kidney_disease",
            "model_version": "v1.0_mock",
            "scan_quality": "Good"
        }
    
    @staticmethod
    def predict_liver_disease(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Liver disease screening based on lab values
        Uses liver enzyme levels and protein markers
        """
        age = int(data.get('age', 40))
        total_bilirubin = float(data.get('total_bilirubin', 0.7))
        alkaline_phosphotase = int(data.get('alkaline_phosphotase', 70))
        alamine_aminotransferase = int(data.get('alamine_aminotransferase', 25))  # ALT
        aspartate_aminotransferase = int(data.get('aspartate_aminotransferase', 25))  # AST
        
        risk_score = 0.0
        factors = []
        
        # Bilirubin (elevated indicates liver dysfunction)
        if total_bilirubin >= 2.0:
            risk_score += 0.35
            factors.append(f"Elevated bilirubin ({total_bilirubin} mg/dL) - liver dysfunction indicator")
        elif total_bilirubin >= 1.2:
            risk_score += 0.18
            factors.append(f"Borderline bilirubin ({total_bilirubin} mg/dL)")
        
        # ALT (liver-specific enzyme)
        if alamine_aminotransferase >= 100:
            risk_score += 0.30
            factors.append(f"Very high ALT ({alamine_aminotransferase} U/L) - significant liver damage")
        elif alamine_aminotransferase >= 60:
            risk_score += 0.20
            factors.append(f"Elevated ALT ({alamine_aminotransferase} U/L) - liver inflammation")
        
        # AST 
        if aspartate_aminotransferase >= 100:
            risk_score += 0.25
            factors.append(f"Very high AST ({aspartate_aminotransferase} U/L)")
        elif aspartate_aminotransferase >= 60:
            risk_score += 0.15
            factors.append(f"Elevated AST ({aspartate_aminotransferase} U/L)")
        
        # Alkaline Phosphatase
        if alkaline_phosphotase >= 150:
            risk_score += 0.15
            factors.append(f"High ALP ({alkaline_phosphotase} U/L) - possible cholestasis")
        
        risk_score = min(risk_score, 1.0)
        
        # Classification
        if risk_score >= 0.60:
            prediction = "High Risk - Liver Disease Likely"
            recommendation = "🔴 URGENT: Consult hepatologist. Further testing (ultrasound, fibroscan) required."
            color = "red"
        elif risk_score >= 0.35:
            prediction = "Moderate Risk - Abnormal Liver Function"
            recommendation = "See doctor within 1 week. Repeat liver function tests. Avoid alcohol."
            color = "orange"
        elif risk_score >= 0.15:
            prediction = "Mild Elevation"
            recommendation = "Monitor liver enzymes. Lifestyle modifications recommended."
            color = "orange"
        else:
            prediction = "Normal Liver Function"
            recommendation = "Liver enzymes within healthy range. Continue healthy habits."
            color = "green"
        
        confidence = 0.85 + (abs(risk_score - 0.5) * 0.22)
        
        if not factors:
            factors.append("All liver markers within normal range")
        
        return {
            "prediction": prediction,
            "risk_score": round(risk_score, 3),
            "confidence": round(confidence, 3),
            "risk_factors": factors,
            "recommendation": recommendation,
            "color": color,
            "model_name": "liver_disease",
            "model_version": "v1.0_enhanced"
        }
    
    @staticmethod
    def predict_breast_cancer(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Breast cancer classification based on cell nucleus measurements
        Simplified version of Wisconsin Breast Cancer dataset features
        """
        # Using subset of features for simplicity
        texture_mean = float(data.get('texture_mean', 15))
        perimeter_mean = float(data.get('perimeter_mean', 80))
        area_mean = float(data.get('area_mean', 500))
        concavity_mean = float(data.get('concavity_mean', 0.1))
        
        malignancy_score = 0.0
        
        # Texture (roughness of nucleus)
        if texture_mean >= 25:
            malignancy_score += 0.25
        elif texture_mean >= 20:
            malignancy_score += 0.12
        
        # Perimeter (larger = more concerning)
        if perimeter_mean >= 120:
            malignancy_score += 0.30
        elif perimeter_mean >= 100:
            malignancy_score += 0.18
        
        # Area
        if area_mean >= 900:
            malignancy_score += 0.28
        elif area_mean >= 700:
            malignancy_score += 0.15
        
        # Concavity (indentations)
        if concavity_mean >= 0.20:
            malignancy_score += 0.22
        elif concavity_mean >= 0.12:
            malignancy_score += 0.10
        
        malignancy_score = min(malignancy_score, 1.0)
        
        # Classification
        if malignancy_score >= 0.60:
            prediction = "Malignant"
            recommendation = "⚠️ URGENT: High likelihood of malignancy. Immediate oncologist consultation and biopsy required."
            color = "red"
        elif malignancy_score >= 0.35:
            prediction = "Suspicious"
            recommendation = "Concerning features detected. Schedule biopsy and further testing within 1 week."
            color = "orange"
        else:
            prediction = "Benign"
            recommendation = "Likely benign. Regular monitoring recommended. Follow-up in 6 months."
            color = "green"
        
        confidence = 0.88 + (abs(malignancy_score - 0.5) * 0.18)
        
        return {
            "prediction": prediction,
            "malignancy_score": round(malignancy_score, 3),
            "confidence": round(confidence, 3),
            "recommendation": recommendation,
            "color": color,
            "model_name": "breast_cancer",
            "model_version": "v1.0_wisconsin"
        }
    
    @staticmethod
    def predict_parkinsons(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parkinson's disease detection from voice measurements
        Based on dysphonia features (jitter, shimmer, etc.)
        """
        jitter = float(data.get('mdvp_jitter', 0.005))  # Frequency variation
        shimmer = float(data.get('shimmer', 0.03))  # Amplitude variation
        nhr = float(data.get('nhr', 0.02))  # Noise-to-harmonics ratio
        hnr = float(data.get('hnr', 22))  # Harmonics-to-noise ratio
        
        parkinsons_score = 0.0
        indicators = []
        
        # Jitter (higher = more vocal instability, PD indicator)
        if jitter >= 0.010:
            parkinsons_score += 0.30
            indicators.append(f"High voice jitter ({jitter:.4f}) - vocal instability detected")
        elif jitter >= 0.007:
            parkinsons_score += 0.15
            indicators.append(f"Elevated jitter ({jitter:.4f})")
        
        # Shimmer (amplitude variation)
        if shimmer >= 0.08:
            parkinsons_score += 0.28
            indicators.append(f"High shimmer ({shimmer:.3f}) - amplitude variation")
        elif shimmer >= 0.05:
            parkinsons_score += 0.12
            indicators.append(f"Elevated shimmer ({shimmer:.3f})")
        
        # NHR (noise to harmonics)
        if nhr >= 0.05:
            parkinsons_score += 0.25
            indicators.append(f"High NHR ({nhr:.3f}) - increased breathiness")
        elif nhr >= 0.03:
            parkinsons_score += 0.10
            indicators.append(f"Elevated NHR ({nhr:.3f})")
        
        # HNR (lower = more noise, PD indicator)
        if hnr <= 18:
            parkinsons_score += 0.20
            indicators.append(f"Low HNR ({hnr:.1f} dB) - reduced voice quality")
        elif hnr <= 21:
            parkinsons_score += 0.08
            indicators.append(f"Borderline HNR ({hnr:.1f} dB)")
        
        parkinsons_score = min(parkinsons_score, 1.0)
        
        # Classification
        if parkinsons_score >= 0.65:
            prediction = "Parkinson's Likely"
            recommendation = "⚠️ URGENT: Strong indicators of Parkinson's disease. Consult neurologist for clinical evaluation and DAT scan."
            color = "red"
        elif parkinsons_score >= 0.40:
            prediction = "Parkinson's Possible"
            recommendation = "Voice abnormalities detected. Neurological assessment recommended. Monitor symptoms."
            color = "orange"
        else:
            prediction = "No Parkinson's Detected"
            recommendation = "Voice measurements within normal range. Continue regular health monitoring."
            color = "green"
        
        confidence = 0.80 + (abs(parkinsons_score - 0.5) * 0.28)
        
        if not indicators:
            indicators.append("All voice measurements within healthy parameters")
        
        return {
            "prediction": prediction,
            "parkinsons_score": round(parkinsons_score, 3),
            "confidence": round(confidence, 3),
            "indicators": indicators,
            "recommendation": recommendation,
            "color": color,
            "model_name": "parkinsons",
            "model_version": "v1.0_voice"
        }


# Singleton instance
mock_engine = MockPredictionEngine()
