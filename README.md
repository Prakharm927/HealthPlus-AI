# OpenHealth: Production-Grade AI Health Prediction Service

[![CI/CD Pipeline](https://github.com/yourusername/OpenHealth/workflows/CI/CD%20Pipeline/badge.svg)](https://github.com/yourusername/OpenHealth/actions)
[![Docker Build](https://img.shields.io/docker/build/yourusername/openhealth)](https://hub.docker.com/r/yourusername/openhealth)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

<img src="static/images/Logo.png" alt="OpenHealth Logo" width="200"/>

## 🎯 The Problem

**How do AI startups deploy multi-disease prediction models at scale in production?**

Most health AI projects end as Jupyter notebooks. This project demonstrates how a real health-tech startup would operationalize AI predictions:
- **Not a script** → Service-oriented API architecture  
- **Not a demo** → Production-ready with monitoring, versioning, and failure handling
- **Not fire-and-forget** → Continuous validation with drift detection and fallback logic

## 🚀 What Makes This Production-Grade?

### ✅ Built for Operations Teams, Not Data Scientists

| Feature | Why It Matters | Implementation |
|---------|----------------|----------------|
| **FastAPI Service** | Ops teams deploy services, not notebooks | REST API with `/predict`, `/health`, `/model-info` |
| **Model Versioning** | Safe rollbacks when models break | Version registry with `v1`, `v2`, rollback endpoint |
| **Monitoring** | AI breaks silently—you need visibility | Latency tracking, confidence logging, drift detection |
| **Failure Handling** | Low-confidence predictions need fallbacks | Threshold-based safe responses, retraining alerts |
| **CI/CD Pipeline** | Automated testing prevents regressions | GitHub Actions: lint →  test → Docker build → deploy |
| **Docker Deployment** | Reproducible across environments | Multi-stage Dockerfile, <500MB image |

### 📊 Supported Disease Predictions

- **Brain Tumor Detection** (MRI scans) - Glioma, Meningioma, Pituitary, No Tumor
- **Heart Disease Risk** (clinical parameters) - Risk score with 13 features
- **Diabetes Prediction** (patient data) - Diabetic vs Non-Diabetic
- **Kidney Disease** (CT scans) - Cyst, Normal, Stone, Tumor
- **Liver Disease** (lab results) - Positive/Negative
- **Breast Cancer** (cell nucleus features) - Malignant/Benign
- **Parkinson's Disease** (voice measurements) - Detected/Not Detected

## 🏃 Quick Start (3 Commands)

```bash
# 1. Clone and navigate
git clone https://github.com/yourusername/OpenHealth.git
cd OpenHealth

# 2. Build and run with Docker
docker-compose up --build

# 3. Access the API
open http://localhost:8000/docs
```

**That's it.** Service is running with live API documentation at `/docs`.

## 📚 API Documentation

### Health Checks
```bash
GET /health          # Service status
GET /ready           # Readiness probe
GET /model-info      # Model versions and metadata
GET /metrics         # Performance metrics
```

### Predictions
```bash
POST /predict/brain-tumor      # MRI → Tumor type
POST /predict/heart-disease    # Clinical params → Risk score
POST /predict/diabetes         # Patient data → Diabetic risk
POST /predict/kidney-disease   # CT scan → Condition
POST /predict/liver-disease    # Lab results → Disease status
POST /predict/breast-cancer    # Cell features → Cancer detection
POST /predict/parkinsons       # Voice data → Parkinson's detection
```

### Admin (Model Management)
```bash
POST /admin/reload-model/{model_name}         # Reload from disk
POST /admin/rollback/{model_name}             # Revert to previous version
POST /admin/set-version/{model_name}/{version} # Switch  to specific version
GET  /admin/cache-info                        # View cached models
POST /admin/clear-cache                       # Clear model cache
```

**Example Request:**
```bash
curl -X POST "http://localhost:8000/predict/heart-disease" \
  -H "Content-Type: application/json" \
  -d '{
    "age": 63, "sex": 1, "cp": 3, "trestbps": 145,
    "chol": 233, "fbs": 1, "restecg": 0, "thalach": 150,
    "exang": 0, "oldpeak": 2.3, "slope": 0, "ca": 0, "thal": 1
  }'
```

**Response:**
```json
{
  "prediction": "High Risk",
  "confidence": 0.87,
  "model_version": "v1",
  "model_name": "heart",
  "fallback_used": false,
  "timestamp": "2026-01-05T16:20:00",
  "metadata": {"risk_score": 0.87}
}
```

## 🏗️ Architecture

```
┌─────────────┐         ┌──────────────────┐         ┌─────────────────┐
│  Client     │────────▶│   FastAPI App    │────────▶│  Model Loader   │
│  (REST API) │         │  (main.py)       │         │  (Singleton)    │
└─────────────┘         └──────────────────┘         └─────────────────┘
                                │                              │
                                ▼                              ▼
                        ┌──────────────────┐         ┌─────────────────┐
                        │  Monitoring      │         │ Model Registry  │
                        │  - Metrics       │         │ - Versions      │
                        │  - Logging       │         │ - Metadata      │
                        │  - Drift Detect  │         │ - Rollback      │
                        └──────────────────┘         └─────────────────┘
```

## 🛡️ Failure Scenarios & Safeguards

### 1. Low Confidence Predictions
**Problem**: Model returns 65% confidence (below 75% threshold)  
**Safeguard**: Return "Uncertain - please consult healthcare professional" + log event for retraining

### 2. Model Load Failure
**Problem**: Model file corrupted or missing  
**Safeguard**: Graceful degradation with 503 Service Unavailable + detailed error logging

### 3. Data Quality Issues
**Problem**: Incoming data has NaN values or outliers  
**Safeguard**: Validation layer rejects bad data with 422 Unprocessable Entity

### 4. Data Drift Detected
**Problem**: Input distribution shifts significantly from training data  
**Safeguard**: Drift detector alerts via logs + flags for model retraining

### 5. Model Regression After Update
**Problem**: New model version underperforms  
**Safeguard**: One-command rollback via `/admin/rollback/{model}` endpoint

## 📈 How This Scales

### Current Architecture (Single Instance)
- ✅ Handles 100-500 req/sec on modest hardware
- ✅ Model caching prevents redundant loading
- ✅ Async FastAPI for concurrent requests

### Horizontal Scaling (Production)
```yaml
# Kubernetes deployment (example)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: openhealth-api
spec:
  replicas: 5  # Scale to 5 instances
  selector:
    matchLabels:
      app: openhealth
  template:
    spec:
      containers:
      - name: api
        image: openhealth:latest
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
```

### Future Optimizations
- **Model Serving Layer**: Separate model serving with TensorFlow Serving or TorchServe
- **Async Predictions**: Queue-based system (Celery + Redis) for batch processing
- **Edge Deployment**: TensorFlow Lite models for on-device inference

## 🧪 Development Setup

### Local Python Environment
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Copy environment template
cp .env.example .env
# Edit .env with your configuration

# Run development server
uvicorn src.api.main:app --reload

# Run tests
pytest
pytest -v --cov=src  # With coverage
```

### Manual Docker Build
```bash
# Build image
docker build -t openhealth:latest .

# Run container
docker run -p 8000:8000 \
  -e MODEL_VERSION=v1 \
  -e CONFIDENCE_THRESHOLD=0.75 \
  -v $(pwd)/models:/app/models \
  openhealth:latest
```

## 🔍 Monitoring & Observability

### Available Metrics
```bash
curl http://localhost:8000/metrics
```

Returns:
- **Latency stats** (p50, p95, p99) per model
- **Prediction counts** (success/failure) per endpoint
- **Confidence scores** (mean, min, max)  
- **Low confidence events** for retraining triggers

### Structured Logging
All logs in JSON format for easy parsing:
```json
{
  "timestamp": "2026-01-05T16:20:00",
  "level": "INFO",
  "message": "Heart disease prediction: High Risk",
  "request_id": "abc123",
  "model_name": "heart",
  "confidence": 0.87,
  "latency_ms": 45.3
}
```

### Data Drift Detection
```python
# Automatic drift detection on predictions
# Alert when distribution shifts > 30% from training data
# Logged events trigger retraining workflows
```

## 🤝 Production Checklist

Before deploying to production:

- [ ] Environment variables configured (`.env` file)
- [ ] Model artifacts present in `models/v1/` directory
- [ ] Health checks passing (`/health` returns 200)
- [ ] Tests passing (`pytest` all green)
- [ ] Docker image builds successfully
- [ ] CI/CD pipeline configured (GitHub Actions)
- [ ] Monitoring enabled (`MONITORING_ENABLED=true`)
- [ ] Confidence thresholds tuned per model
- [ ] Load testing completed (optional but recommended)

## 🧩 Project Structure

```
OpenHealth/
├── src/
│   ├── api/                    # FastAPI application
│   │   ├── main.py            # Main app, middleware, error handling
│   │   ├── schemas.py         # Pydantic request/response models
│   │   └── routers/           # Route handlers
│   │       ├── health.py      # Health checks & monitoring
│   │       ├── predictions.py # Prediction endpoints
│   │       └── admin.py       # Model management
│   ├── models/                # Model management
│   │   ├── registry.py        # Version tracking, rollback
│   │   └── loader.py          # Lazy loading, caching
│   ├── monitoring/            # Observability
│   │   ├── logger.py          # Structured JSON logging
│   │   ├── metrics.py         # Latency, counts, confidence tracking
│   │   └── drift_detector.py # Data distribution monitoring
│   └── data/                  # Data pipeline
│       └── validators.py      # Input validation, quality checks
├── config/
│   └── settings.py            # Environment-based configuration
├── models/
│   ├── v1/                    # Versioned model storage
│   └── active_versions.json  # Version tracking
├── tests/
│   ├── unit/                  # Unit tests
│   ├── integration/           # Integration tests
│   └── conftest.py            # Test fixtures
├── .github/workflows/
│   └── ci.yml                 # CI/CD pipeline
├── Dockerfile                 # Multi-stage production build
├── docker-compose.yml         # Local development
├── requirements.txt           # Production dependencies
├── requirements-dev.txt       # Development dependencies
└── pytest.ini                 # Test configuration
```

## 🤖 CI/CD Pipeline

Every push triggers:
1. **Linting**: Black, flake8, isort, mypy
2. **Testing**: Unit + integration tests with coverage
3. **Model Validation**: Verify artifacts exist and loadable
4. **Docker Build**: Multi-stage build with caching
5. **Version Tagging**: Auto-increment on main branch

View pipeline: `.github/workflows/ci.yml`

## 📝 License

GNU General Public License v3.0 - see [LICENSE](LICENSE) file.

## 🙏 Acknowledgements

Built to demonstrate production-grade AI Operations for health-tech startups. Inspired by real-world deployments at cloud-native AI companies.

**Original Research**: Models based on public health datasets and academic research.

## 📧 Contact

**Questions about AI Operations or deployment strategies?**

- Email: [your-email@example.com](mailto:your-email@example.com)
- LinkedIn: [Your Name](#)
- Project Issues: [GitHub Issues](https://github.com/yourusername/OpenHealth/issues)

---

**⚡ Built for AI Operations internships** - Showcasing production deployment, monitoring, version control, and failure handling that 90% of student projects lack.
