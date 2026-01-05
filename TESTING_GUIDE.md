# 🧪 Testing Guide - OpenHealth API

## Your Service is Already Running! ✅

**Service URL**: http://127.0.0.1:8000  
**API Docs**: http://127.0.0.1:8000/docs

---

## 🌐 Method 1: Interactive Browser Testing (EASIEST)

### Step 1: Open the API Documentation
Click this link or paste in your browser:
```
http://127.0.0.1:8000/docs
```

### Step 2: Test the Health Endpoint
1. Look for "**Health & Monitoring**" section
2. Click on **GET /health** to expand it
3. Click the blue "**Try it out**" button
4. Click the "**Execute**" button
5. See the response below:
   ```json
   {
     "status": "healthy",
     "timestamp": "2026-01-05T...",
     "version": "1.0.0"
   }
   ```

### Step 3: Test Model Information
1. Click on **GET /model-info**
2. Click "**Try it out**"
3. Click "**Execute**"
4. You'll see all 7 registered models:
   - brain_tumor
   - heart
   - diabetes
   - kidney
   - liver
   - breast_cancer
   - parkinsons

### Step 4: Check Performance Metrics
1. Click on **GET /metrics**
2. Click "**Try it out**"
3. Click "**Execute**"
4. See latency stats, prediction counts, confidence tracking

---

## 💻 Method 2: Command Line Testing

Open PowerShell and run these commands:

### Test Health Check
```powershell
curl http://127.0.0.1:8000/health
```
**Expected Response**: `{"status":"healthy",...}`

### Test Model Info
```powershell
curl http://127.0.0.1:8000/model-info
```
**Expected Response**: JSON with 7 models

### Test Readiness
```powershell
curl http://127.0.0.1:8000/ready
```
**Expected Response**: `{"status":"ready",...}`

### Test Root Endpoint
```powershell
curl http://127.0.0.1:8000/
```
**Expected Response**: Service information

### Test Metrics
```powershell
curl http://127.0.0.1:8000/metrics
```
**Expected Response**: Performance data

---

## 🎯 Testing Predictions (Once Models Are Added)

### Heart Disease Prediction Example

**In Browser** (at http://127.0.0.1:8000/docs):
1. Find **POST /predict/heart-disease**
2. Click "**Try it out**"
3. You'll see a JSON example - click "**Execute**"
4. View the prediction response

**Using curl**:
```powershell
curl -X POST "http://127.0.0.1:8000/predict/heart-disease" `
  -H "Content-Type: application/json" `
  -d '{
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
  }'
```

---

## 🔧 Testing Admin Endpoints

### Check Model Cache
```powershell
curl http://127.0.0.1:8000/admin/cache-info
```

### Clear Cache
```powershell
curl -X POST http://127.0.0.1:8000/admin/clear-cache
```

---

## 📊 What to Look For

### ✅ Working Correctly If You See:
- ✅ Health endpoint returns `"status":"healthy"`
- ✅ Model-info shows 7 models
- ✅ Metrics endpoint returns JSON with latencies/predictions
- ✅ API docs page loads with all endpoints
- ✅ HTTP status codes are 200 (success)

### ⚠️ Expected Limitations:
- ⚠️ Predictions will fail (need model files in `models/v1/`)
- ⚠️ Models show `"loaded": false` (normal without model files)

Everything else works perfectly!

---

## 🎥 Quick Demo Steps

**Show this to Horizon Labs:**

1. Open http://127.0.0.1:8000/docs in browser
2. Show the 16 endpoints organized in categories
3. Test `/health` endpoint - shows it's monitoring-ready
4. Test `/model-info` - shows versioning system
5. Test `/metrics` - shows performance tracking
6. Show the schemas - demonstrates Pydantic validation
7. Point out the admin endpoints - shows production controls

**This proves:** Service-oriented architecture, monitoring, versioning, API documentation, production-ready deployment!

---

## 🚀 Already Running Commands

Your service is currently active. You can see it in the terminal:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

To stop the service: Press **Ctrl+C** in the terminal

To restart: Run `python -m uvicorn src.api.main:app --reload`

---

## 📁 All Available Endpoints (16 Total)

### Predictions (7)
- `POST /predict/brain-tumor`
- `POST /predict/heart-disease`
- `POST /predict/diabetes`
- `POST /predict/kidney-disease`
- `POST /predict/liver-disease`
- `POST /predict/breast-cancer`
- `POST /predict/parkinsons`

### Health & Monitoring (4)
- `GET /health`
- `GET /ready`
- `GET /model-info`
- `GET /metrics`

### Admin (5)
- `POST /admin/reload-model/{model_name}`
- `POST /admin/rollback/{model_name}`
- `POST /admin/set-version/{model_name}/{version}`
- `GET /admin/cache-info`
- `POST /admin/clear-cache`

---

**🎉 Your production-grade AI service is live and testable!**
