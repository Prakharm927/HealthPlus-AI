@echo off
REM OpenHealth FastAPI Server Startup Script

echo Starting OpenHealth AI Service...
echo.

REM Check if .env exists
if not exist .env (
    echo Creating .env from template...
    copy .env.example .env
)

echo.
echo Starting FastAPI server...
echo API Documentation will be available at: http://localhost:8000/docs
echo.

python -m uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
