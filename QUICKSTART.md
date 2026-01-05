# OpenHealth Production Transformation - Quick Start Guide

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Docker & Docker Compose
- Git

### Option 1: Docker (Recommended)

```bash
# 1. Navigate to project
cd "c:/Users/prakh/OneDrive/Desktop/health ai/OpenHealth"

# 2. Build and run
docker-compose up --build

# 3. Access API
# Open browser to: http://localhost:8000/docs
```

### Option 2: Local Python Environment

```bash
# 1. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Copy environment template
copy .env.example .env

# 4. Run development server
python -m uvicorn src.api.main:app --reload

# 5. Access API
# Open browser to: http://localhost:8000/docs
```

## 📝 Important Notes

### Model Artifacts
⚠️ **Model files are not included** - You need to either:

1. **Copy existing models** (if you have them):
   ```bash
   # Copy from Artifacts/ to models/v1/
   copy "Artifacts\Brain_Tumour\BrainModel.h5" "models\v1\brain_tumor.h5"
   copy "Artifacts\Kidney_Disease\Kidney_Model.h5" "models\v1\kidney.h5"
   copy "Artifacts\Liver_Disease\Liver_Model.pkl" "models\v1\liver.pkl"
   # ... and so on
   ```

2. **Retrain from notebooks**:
   - Run notebooks in `Notebook_Experiments/`
   - Save models to `models/v1/`

3. **For testing only**: The service will start without models but predictions will fail

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-cov httpx

# Run all tests
pytest

# Run with coverage
pytest -v --cov=src
```

## 🔍 Verify Installation

```bash
# Health check
curl http://localhost:8000/health

# Model info
curl http://localhost:8000/model-info

# API docs
# Visit: http://localhost:8000/docs
```

## 📚 Next Steps

1. Review the [walkthrough](file:///C:/Users/prakh/.gemini/antigravity/brain/4df20f07-85c8-4c3d-86ca-fbaa668fab23/walkthrough.md)
2. Check out the [implementation plan](file:///C:/Users/prakh/.gemini/antigravity/brain/4df20f07-85c8-4c3d-86ca-fbaa668fab23/implementation_plan.md)
3. Read the production [README](file:///c:/Users/prakh/OneDrive/Desktop/health%20ai/OpenHealth/README.md)
4. Test prediction endpoints at `/docs`
5. Explore monitoring at `/metrics`
