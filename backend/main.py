"""
FastAPI Backend - Network Traffic Classifier
Prediction API for the trained model
"""

from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import joblib
import numpy as np
from datetime import datetime
from pathlib import Path
import json
import sys
import logging
import logging.handlers

# Add project root to path for config imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import (
    MODEL_PATH, SCALER_PATH, ENCODER_PATH, METADATA_PATH,
    CORS_ORIGINS, CORS_CREDENTIALS, CORS_METHODS, CORS_HEADERS,
    API_KEY, LOG_API_FILE, LOG_PREDICTIONS_FILE, LOG_LEVEL, LOG_FORMAT
)

# Initialize FastAPI app
app = FastAPI(
    title="AI Network Traffic Classifier",
    description="ML-powered network traffic classification API",
    version="1.0.0"
)

# ============================================================================
# LOGGING SETUP
# ============================================================================

def setup_logging():
    """Configure structured logging"""
    LOG_API_FILE.parent.mkdir(exist_ok=True)
    api_logger = logging.getLogger("api")
    api_logger.setLevel(logging.INFO)
    api_handler = logging.handlers.RotatingFileHandler(
        LOG_API_FILE, maxBytes=10485760, backupCount=5
    )
    api_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    api_logger.addHandler(api_handler)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, LOG_LEVEL))
    console_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    api_logger.addHandler(console_handler)
    
    pred_logger = logging.getLogger("predictions")
    pred_logger.setLevel(logging.INFO)
    pred_handler = logging.handlers.RotatingFileHandler(
        LOG_PREDICTIONS_FILE, maxBytes=10485760, backupCount=5
    )
    pred_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    pred_logger.addHandler(pred_handler)
    return api_logger, pred_logger

api_logger, pred_logger = setup_logging()

# ============================================================================
# AUTHENTICATION (Bypassed if no API_KEY set)
# ============================================================================

# async def verify_api_key(x_api_key: str = Header(None)):
#     """Bypass authentication if API_KEY is not configured."""
#     if not API_KEY:
#         return x_api_key
#     if not x_api_key or x_api_key != API_KEY:
#         api_logger.warning(f"Invalid API key: {x_api_key[:10] if x_api_key else 'None'}...")
#         raise HTTPException(status_code=403, detail="Invalid or missing API key")
#     return x_api_key

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in CORS_ORIGINS],
    allow_credentials=CORS_CREDENTIALS,
    allow_methods=CORS_METHODS,
    allow_headers=CORS_HEADERS,
)

# Global model variables
model = None
scaler = None
encoder = None
metadata = None
model_loaded = False

# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class PredictionRequest(BaseModel):
    duration: float = Field(..., ge=0, le=86400)
    protocol_type: str
    service: str
    flag: str
    src_bytes: float = Field(..., ge=0)
    dst_bytes: float = Field(..., ge=0)
    land: int = Field(..., ge=0, le=1)
    wrong_fragment: int = Field(..., ge=0, le=100)
    urgent: int = Field(..., ge=0, le=100)
    hot: int = Field(..., ge=0, le=100)
    num_failed_logins: int = Field(..., ge=0, le=5)
    logged_in: int = Field(..., ge=0, le=1)
    num_compromised: int = Field(..., ge=0, le=1000)
    root_shell: int = Field(..., ge=0, le=1)
    su_attempted: int = Field(..., ge=0, le=1)
    num_root: int = Field(..., ge=0, le=1000)
    num_file_creations: int = Field(..., ge=0, le=1000)
    num_shells: int = Field(..., ge=0, le=1000)
    num_access_files: int = Field(..., ge=0, le=1000)
    num_outbound_cmds: int = Field(..., ge=0, le=1000)
    is_host_login: int = Field(..., ge=0, le=1)
    is_guest_login: int = Field(..., ge=0, le=1)
    count: int = Field(..., ge=1, le=511)
    srv_count: int = Field(..., ge=1, le=511)
    serror_rate: float = Field(..., ge=0.0, le=1.0)
    srv_serror_rate: float = Field(..., ge=0.0, le=1.0)
    rerror_rate: float = Field(..., ge=0.0, le=1.0)
    srv_rerror_rate: float = Field(..., ge=0.0, le=1.0)
    same_srv_rate: float = Field(..., ge=0.0, le=1.0)
    same_ctry_rate: float = Field(..., ge=0.0, le=1.0)
    dst_host_count: int = Field(..., ge=1, le=255)
    dst_host_srv_count: int = Field(..., ge=1, le=255)
    dst_host_same_srv_rate: float = Field(..., ge=0.0, le=1.0)
    dst_host_diff_srv_rate: float = Field(..., ge=0.0, le=1.0)
    dst_host_same_src_port_rate: float = Field(..., ge=0.0, le=1.0)
    dst_host_srv_diff_host_rate: float = Field(..., ge=0.0, le=1.0)
    dst_host_serror_rate: float = Field(..., ge=0.0, le=1.0)
    dst_host_srv_serror_rate: float = Field(..., ge=0.0, le=1.0)
    dst_host_rerror_rate: float = Field(..., ge=0.0, le=1.0)
    dst_host_srv_rerror_rate: float = Field(..., ge=0.0, le=1.0)

class PredictionResponse(BaseModel):
    prediction: str
    confidence: float
    timestamp: str
    probabilities: dict = None

class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    version: str

# ============================================================================
# STARTUP
# ============================================================================

@app.on_event("startup")
async def load_model_on_startup():
    global model, scaler, encoder, metadata, model_loaded
    try:
        print("\n🔄 Loading model...")
        model = joblib.load(MODEL_PATH)
        scaler = joblib.load(SCALER_PATH)
        encoder = joblib.load(ENCODER_PATH)
        with open(METADATA_PATH, 'r') as f:
            metadata = json.load(f)
        model_loaded = True
        print("✅ Model loaded successfully!")
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        model_loaded = False

# ============================================================================
# ROUTES
# ============================================================================

@app.get("/", tags=["info"])
async def root():
    return {"name": "AI Network Traffic Classifier", "version": "1.0.0", "status": "online"}

@app.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="online" if model_loaded else "offline",
        model_loaded=model_loaded,
        version="1.0.0"
    )

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    if not model_loaded or model is None:
        api_logger.error("Model not loaded")
        raise HTTPException(status_code=503, detail="Model not loaded")
    try:
        # Build feature array in the exact order expected by the model
        features = [
            request.duration,
            request.protocol_type,
            request.service,
            request.flag,
            request.src_bytes,
            request.dst_bytes,
            request.land,
            request.wrong_fragment,
            request.urgent,
            request.hot,
            request.num_failed_logins,
            request.logged_in,
            request.num_compromised,
            request.root_shell,
            request.su_attempted,
            request.num_root,
            request.num_file_creations,
            request.num_shells,
            request.num_access_files,
            request.num_outbound_cmds,
            request.is_host_login,
            request.is_guest_login,
            request.count,
            request.srv_count,
            request.serror_rate,
            request.srv_serror_rate,
            request.rerror_rate,
            request.srv_rerror_rate,
            request.same_srv_rate,
            request.same_ctry_rate,
            request.dst_host_count,
            request.dst_host_srv_count,
            request.dst_host_same_srv_rate,
            request.dst_host_diff_srv_rate,
            request.dst_host_same_src_port_rate,
            request.dst_host_srv_diff_host_rate,
            request.dst_host_serror_rate,
            request.dst_host_srv_serror_rate,
            request.dst_host_rerror_rate,
            request.dst_host_srv_rerror_rate
        ]
        import pandas as pd
        df = pd.DataFrame([features], columns=metadata['features'])
        X_scaled = scaler.transform(df)
        pred_class = model.predict(X_scaled)[0]
        pred_label = encoder.classes_[pred_class]
        probs = model.predict_proba(X_scaled)[0]
        proba_dict = {label: float(prob) for label, prob in zip(encoder.classes_, probs)}
        confidence = float(np.max(probs))
        api_logger.info(f"Prediction: {pred_label} ({confidence:.2%})")
        return PredictionResponse(
            prediction=pred_label,
            confidence=confidence,
            timestamp=datetime.utcnow().isoformat(),
            probabilities=proba_dict
        )
    except Exception as e:
        api_logger.error(f"Prediction error: {e}", exc_info=True)
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/info")
async def get_info():
    if not model_loaded:
        raise HTTPException(status_code=503, detail="Model not loaded")
    return {
        "features": metadata['features'],
        "classes": metadata['classes'],
        "metrics": metadata['metrics']
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)