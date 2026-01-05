# OpenHealth Models Directory

This directory contains versioned model artifacts for the OpenHealth AI service.

## Structure

```
models/
├── v1/                      # Version 1 models
│   ├── brain_tumor.h5      # Brain tumor detection model
│   ├── kidney.h5           # Kidney disease detection model
│   ├── liver.pkl           # Liver disease prediction model
│   ├── heart.pkl           # Heart disease risk model
│   ├── diabetes.pkl        # Diabetes prediction model
│   ├── breast_cancer.pkl   # Breast cancer detection model
│   └── parkinsons.pkl      # Parkinson's disease detection model
├── v2/                      # Future version 2 models
├── reference_stats/         # Reference statistics for drift detection
└── active_versions.json     # Active version tracking
```

## Adding New Models

To add new model versions:

1. Create a new version directory (e.g., `v2/`)
2. Place model files with standardized names
3. Create metadata JSON files for each model
4. Update `active_versions.json` or use the admin API

## Model Metadata Format

Each model should have a corresponding `{model_name}_metadata.json` file:

```json
{
  "name": "brain_tumor",
  "version": "v1",
  "created_at": "2026-01-05T16:00:00",
  "model_type": "tensorflow",
  "metrics": {
    "accuracy": 0.95,
    "precision": 0.93,
    "recall": 0.94
  },
  "description": "Brain tumor classification using InceptionV3"
}
```

## Important Notes

⚠️ **Model Files Missing**: This directory structure is created automatically. You need to:

1. **Option 1**: Copy existing model files from `Artifacts/` (if they exist)
2. **Option 2**: Retrain models using notebooks in `Notebook_Experiments/`
3. **Option 3**: Use placeholder/mock models for testing

The application will create this directory structure on first run if it doesn't exist.
