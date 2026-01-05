"""
HealthPlus AI FastAPI Application
Production-grade AI service for multi-disease prediction
"""

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
from pathlib import Path
import time
import uuid

from config.settings import get_settings
from src.api.routers import health_router, predictions_router, admin_router, working_predictions_router, extended_predictions_router
from src.monitoring.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager
    Handles startup and shutdown events
    """
    # Startup
    settings = get_settings()
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    
    # Optionally preload models for faster first predictions
    # Uncomment to enable preloading (increases startup time)
    # try:
    #     logger.info("Preloading models...")
    #     model_loader.preload_models()
    #     logger.info("Models preloaded successfully")
    # except Exception as e:
    #     logger.warning(f"Failed to preload some models: {e}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down application")
    model_loader.clear_cache()


# Initialize FastAPI application
settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="""
    Production-grade AI service for multi-disease prediction.
    
    ## Features
    - Multi-disease detection (Brain Tumor, Heart Disease, Diabetes, Kidney, Liver, Breast Cancer, Parkinson's)
    - Model versioning and rollback
    - Real-time monitoring and metrics
    - Confidence-based fallback logic
    - Production-ready deployment
    
    ## Endpoints
    - **/predict/**: Disease prediction endpoints
    - **/health**: Service health checks
    - **/model-info**: Model metadata and versions
    - **/admin/**: Model management (reload, rollback, version switching)
    - **/metrics**: Performance and prediction metrics
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configure templates
templates = Jinja2Templates(directory="templates")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request ID and logging middleware
@app.middleware("http")
async def add_request_id_and_logging(request: Request, call_next):
    """
    Add request ID to each request and log request/response
    """
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    
    # Log request
    logger.info(
        f"Request started: {request.method} {request.url.path}",
        extra={"request_id": request_id}
    )
    
    start_time = time.time()
    
    try:
        response = await call_next(request)
        process_time = (time.time() - start_time) * 1000
        
        # Add custom headers
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = f"{process_time:.2f}ms"
        
        # Log response
        logger.info(
            f"Request completed: {request.method} {request.url.path} - {response.status_code}",
            extra={"request_id": request_id, "latency_ms": process_time}
        )
        
        return response
        
    except Exception as e:
        logger.error(
            f"Request failed: {request.method} {request.url.path} - {str(e)}",
            extra={"request_id": request_id},
            exc_info=True
        )
        raise


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler for unhandled errors
    """
    request_id = getattr(request.state, "request_id", "unknown")
    
    logger.error(
        f"Unhandled exception: {str(exc)}",
        extra={"request_id": request_id},
        exc_info=True
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "detail": str(exc) if settings.debug else "An unexpected error occurred",
            "request_id": request_id
        }
    )


# Include routers
app.include_router(health_router)
app.include_router(predictions_router)
app.include_router(admin_router)
app.include_router(working_predictions_router)  # Working demo endpoints
app.include_router(extended_predictions_router)  # All 7 diseases


# Root endpoint - Dashboard
@app.get("/", response_class=HTMLResponse, tags=["Root"])
async def root(request: Request):
    """
    Main dashboard - Modern UI for HealthPlus AI Service
    """
    return templates.TemplateResponse("dashboard.html", {"request": request})


@app.get("/demo", response_class=HTMLResponse, tags=["Demo"])
async def demo_page(request: Request):
    """
    Interactive demo page - Try predictions live
    """
    return templates.TemplateResponse("demo.html", {"request": request})


# Individual calculator pages
@app.get("/calculators/heart", response_class=HTMLResponse, tags=["Calculators"])
async def heart_calculator(request: Request):
    """Heart Disease Risk Calculator"""
    return templates.TemplateResponse("calculators/heart.html", {"request": request})

@app.get("/calculators/diabetes", response_class=HTMLResponse, tags=["Calculators"])
async def diabetes_calculator(request: Request):
    """Diabetes Risk Calculator"""
    return templates.TemplateResponse("calculators/diabetes.html", {"request": request})

@app.get("/calculators/liver", response_class=HTMLResponse, tags=["Calculators"])
async def liver_calculator(request: Request):
    """Liver Disease Calculator"""
    return templates.TemplateResponse("calculators/liver.html", {"request": request})

@app.get("/calculators/breast-cancer", response_class=HTMLResponse, tags=["Calculators"])
async def breast_cancer_calculator(request: Request):
    """Breast Cancer Calculator"""
    return templates.TemplateResponse("calculators/breast_cancer.html", {"request": request})

@app.get("/calculators/parkinsons", response_class=HTMLResponse, tags=["Calculators"])
async def parkinsons_calculator(request: Request):
    """Parkinson's Disease Calculator"""
    return templates.TemplateResponse("calculators/parkinsons.html", {"request": request})

@app.get("/calculators/kidney", response_class=HTMLResponse, tags=["Calculators"])
async def kidney_calculator(request: Request):
    """Kidney Disease Calculator"""
    return templates.TemplateResponse("calculators/kidney.html", {"request": request})

@app.get("/calculators/brain-tumor", response_class=HTMLResponse, tags=["Calculators"])
async def brain_tumor_calculator(request: Request):
    """Brain Tumor Calculator"""
    return templates.TemplateResponse("calculators/brain_tumor.html", {"request": request})


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "src.api.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )
