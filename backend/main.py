"""
FastAPI Backend - Network Traffic Classifier
Prediction API for the trained model
"""

from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, validator, Field
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
    TRAFFIC_CLASSES, API_KEY, API_KEY_HEADER, FEATURE_RANGES,
    LOG_API_FILE, LOG_PREDICTIONS_FILE, LOG_LEVEL, LOG_FORMAT
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
    # Create logs directory
    LOG_API_FILE.parent.mkdir(exist_ok=True)
    
    # API Logger
    api_logger = logging.getLogger("api")
    api_logger.setLevel(logging.INFO)
    
    # File handler for API logs
    api_handler = logging.handlers.RotatingFileHandler(
        LOG_API_FILE, maxBytes=10485760, backupCount=5  # 10MB per file, keep 5
    )
    api_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    api_logger.addHandler(api_handler)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, LOG_LEVEL))
    console_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    api_logger.addHandler(console_handler)
    
    # Predictions Logger (audit trail)
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
# AUTHENTICATION
# ============================================================================

async def verify_api_key(x_api_key: str = Header(None)):
    """Verify API key for protected endpoints"""
    if not x_api_key or x_api_key != API_KEY:
        api_logger.warning(f"Unauthorized API access attempt. Key: {x_api_key[:10] if x_api_key else 'None'}...")
        raise HTTPException(status_code=403, detail="Invalid or missing API key")
    return x_api_key

# CORS middleware - allow requests from dashboard
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
# PYDANTIC MODELS (Request/Response schemas)
# ============================================================================

class PredictionRequest(BaseModel):
    """Request model for traffic prediction with validation"""
    duration: float = Field(..., ge=0, le=86400, description="Duration in seconds (0-86400)")
    protocol_type: str = Field(..., description="Protocol type (tcp/udp/icmp)")
    service: str = Field(..., description="Service type")
    flag: str = Field(..., description="Connection flag")
    src_bytes: float = Field(..., ge=0, le=10000000, description="Source bytes")
    dst_bytes: float = Field(..., ge=0, le=10000000, description="Destination bytes")
    land: int = Field(..., ge=0, le=1, description="Same src/dst flag")
    wrong_fragment: int = Field(..., ge=0, le=100, description="Wrong fragments")
    urgent: int = Field(..., ge=0, le=100, description="Urgent flags")
    hot: int = Field(..., ge=0, le=100, description="Hot indicators")
    num_failed_logins: int = Field(..., ge=0, le=5, description="Failed login attempts")
    logged_in: int = Field(..., ge=0, le=1, description="Logged in flag")
    num_compromised: int = Field(..., ge=0, le=1000, description="Compromised count")
    root_shell: int = Field(..., ge=0, le=1, description="Root shell flag")
    su_attempted: int = Field(..., ge=0, le=1, description="Su attempt flag")
    num_root: int = Field(..., ge=0, le=1000, description="Root count")
    num_file_creations: int = Field(..., ge=0, le=1000, description="File creations")
    num_shells: int = Field(..., ge=0, le=1000, description="Shell count")
    num_access_files: int = Field(..., ge=0, le=1000, description="Access files count")
    num_outbound_cmds: int = Field(..., ge=0, le=1000, description="Outbound commands")
    is_host_login: int = Field(..., ge=0, le=1, description="Host login flag")
    is_guest_login: int = Field(..., ge=0, le=1, description="Guest login flag")
    count: int = Field(..., ge=1, le=511, description="Connection count")
    srv_count: int = Field(..., ge=1, le=511, description="Service count")
    serror_rate: float = Field(..., ge=0.0, le=1.0, description="Service error rate")
    srv_serror_rate: float = Field(..., ge=0.0, le=1.0, description="Service error rate")
    rerror_rate: float = Field(..., ge=0.0, le=1.0, description="Rejected rate")
    srv_rerror_rate: float = Field(..., ge=0.0, le=1.0, description="Service rejected rate")
    same_srv_rate: float = Field(..., ge=0.0, le=1.0, description="Same service rate")
    same_ctry_rate: float = Field(..., ge=0.0, le=1.0, description="Same country rate")
    dst_host_count: int = Field(..., ge=1, le=255, description="Destination host count")
    dst_host_srv_count: int = Field(..., ge=1, le=255, description="Destination service count")
    dst_host_same_srv_rate: float = Field(..., ge=0.0, le=1.0, description="Same service rate")
    dst_host_diff_srv_rate: float = Field(..., ge=0.0, le=1.0, description="Different service rate")
    dst_host_same_src_port_rate: float = Field(..., ge=0.0, le=1.0, description="Same source port rate")
    dst_host_srv_diff_host_rate: float = Field(..., ge=0.0, le=1.0, description="Different host rate")
    dst_host_serror_rate: float = Field(..., ge=0.0, le=1.0, description="Service error rate")
    dst_host_srv_serror_rate: float = Field(..., ge=0.0, le=1.0, description="Service error rate")
    dst_host_rerror_rate: float = Field(..., ge=0.0, le=1.0, description="Rejected rate")
    dst_host_srv_rerror_rate: float = Field(..., ge=0.0, le=1.0, description="Service rejected rate")
    
    class Config:
        json_schema_extra = {
            "example": {
                "duration": 120,
                "protocol_type": "tcp",
                "service": "http",
                "flag": "S2",
                "src_bytes": 5000,
                "dst_bytes": 4000,
                "land": 0,
                "wrong_fragment": 0,
                "urgent": 0,
                "hot": 0,
                "num_failed_logins": 0,
                "logged_in": 1,
                "num_compromised": 0,
                "root_shell": 0,
                "su_attempted": 0,
                "num_root": 0,
                "num_file_creations": 0,
                "num_shells": 0,
                "num_access_files": 0,
                "num_outbound_cmds": 0,
                "is_host_login": 0,
                "is_guest_login": 0,
                "count": 5,
                "srv_count": 4,
                "serror_rate": 0.02,
                "srv_serror_rate": 0.02,
                "rerror_rate": 0.01,
                "srv_rerror_rate": 0.01,
                "same_srv_rate": 0.95,
                "same_ctry_rate": 0.98,
                "dst_host_count": 10,
                "dst_host_srv_count": 8,
                "dst_host_same_srv_rate": 0.9,
                "dst_host_diff_srv_rate": 0.1,
                "dst_host_same_src_port_rate": 0.95,
                "dst_host_srv_diff_host_rate": 0.05,
                "dst_host_serror_rate": 0.01,
                "dst_host_srv_serror_rate": 0.01,
                "dst_host_rerror_rate": 0.01,
                "dst_host_srv_rerror_rate": 0.01
            }
        }

class PredictionResponse(BaseModel):
    """Response model for predictions"""
    prediction: str
    confidence: float
    timestamp: str
    probabilities: dict = None

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    model_loaded: bool
    version: str

# ============================================================================
# STARTUP - Load model on server start
# ============================================================================

@app.on_event("startup")
async def load_model_on_startup():
    """Load ML model when server starts"""
    global model, scaler, encoder, metadata, model_loaded
    
    try:
        print("\n🔄 Loading model on startup...")
        
        if not MODEL_PATH.exists():
            raise FileNotFoundError(f"Model not found: {MODEL_PATH}")
        
        model = joblib.load(MODEL_PATH)
        scaler = joblib.load(SCALER_PATH)
        encoder = joblib.load(ENCODER_PATH)
        
        with open(METADATA_PATH, 'r') as f:
            metadata = json.load(f)
        
        model_loaded = True
        print("✅ Model loaded successfully!")
        print(f"📊 Model path: {MODEL_PATH}")
        
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        model_loaded = False

# ============================================================================
# ROUTES
# ============================================================================

@app.get("/", tags=["info"])
async def root():
    """Root endpoint"""
    return {
        "name": "AI Network Traffic Classifier",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "online"
    }

@app.get("/health", response_model=HealthResponse, tags=["health"])
async def health_check():
    """Check if API is ready"""
    return HealthResponse(
        status="online" if model_loaded else "offline",
        model_loaded=model_loaded,
        version="1.0.0"
    )

@app.post("/predict", response_model=PredictionResponse, tags=["prediction"])
async def predict(request: PredictionRequest, api_key: str = Depends(verify_api_key)):
    """
    Predict traffic classification
    
    **Authentication:** Requires X-API-Key header
    
    Returns the predicted traffic type and confidence score
    """
    
    if not model_loaded or model is None:
        api_logger.error("Model not loaded when predict called")
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Please check server logs."
        )
    
    try:
        api_logger.info(f"Processing prediction request for {request.protocol_type}/{request.service}")
        
        # Convert request to array in correct order
        features_array = np.array([[
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
            request.dst_host_srv_rerror_rate,
        ]], dtype=object)
        
        # Use metadata features to ensure correct order
        import pandas as pd
        df_sample = pd.DataFrame(features_array, columns=[
            'duration', 'protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes',
            'land', 'wrong_fragment', 'urgent', 'hot', 'num_failed_logins', 'logged_in',
            'num_compromised', 'root_shell', 'su_attempted', 'num_root',
            'num_file_creations', 'num_shells', 'num_access_files', 'num_outbound_cmds',
            'is_host_login', 'is_guest_login', 'count', 'srv_count', 'serror_rate',
            'srv_serror_rate', 'rerror_rate', 'srv_rerror_rate', 'same_srv_rate',
            'same_ctry_rate', 'dst_host_count', 'dst_host_srv_count',
            'dst_host_same_srv_rate', 'dst_host_diff_srv_rate',
            'dst_host_same_src_port_rate', 'dst_host_srv_diff_host_rate',
            'dst_host_serror_rate', 'dst_host_srv_serror_rate',
            'dst_host_rerror_rate', 'dst_host_srv_rerror_rate',
        ])
        
        # Select only features used in training
        X_sample = df_sample[metadata['features']]
        
        # Scale features
        X_scaled = scaler.transform(X_sample)
        
        # Make prediction
        prediction_class = model.predict(X_scaled)[0]
        prediction_label = encoder.classes_[prediction_class]
        
        # Get probabilities
        probabilities = model.predict_proba(X_scaled)[0]
        proba_dict = {
            label: float(prob)
            for label, prob in zip(encoder.classes_, probabilities)
        }
        confidence = float(np.max(probabilities))
        
        # Log prediction
        pred_logger.info(f"Prediction: {prediction_label} (confidence: {confidence:.2%}) | {request.protocol_type}/{request.service}")
        api_logger.info(f"Prediction successful: {prediction_label} ({confidence:.2%})")
        
        return PredictionResponse(
            prediction=prediction_label,
            confidence=confidence,
            timestamp=datetime.utcnow().isoformat(),
            probabilities=proba_dict
        )
        
    except ValueError as e:
        api_logger.error(f"Input validation error: {str(e)}")
        raise HTTPException(status_code=422, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        api_logger.error(f"Prediction error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=400, detail=f"Prediction error: {str(e)}")

@app.get("/info", tags=["info"])
async def get_info():
    """Get model information"""
    if not model_loaded or metadata is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    return {
        "features": metadata['features'],
        "classes": metadata['classes'],
        "metrics": metadata['metrics'],
        "features_count": len(metadata['features']),
        "classes_count": len(metadata['classes'])
    }

@app.get("/features", tags=["info"])
async def get_features():
    """Get required features for prediction"""
    if not model_loaded or metadata is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    return {
        "required_features": metadata['features'],
        "count": len(metadata['features']),
        "example": {
            "duration": 120.5,
            "protocol_type": "tcp",
            "service": "http",
            "flag": "S2",
            "src_bytes": 5000,
            "dst_bytes": 4000,
            "land": 0,
            "wrong_fragment": 0,
            "urgent": 0,
            "hot": 0,
            "num_failed_logins": 0,
            "logged_in": 1,
            "num_compromised": 0,
            "root_shell": 0,
            "su_attempted": 0,
            "num_root": 0,
            "num_file_creations": 0,
            "num_shells": 0,
            "num_access_files": 0,
            "num_outbound_cmds": 0,
            "is_host_login": 0,
            "is_guest_login": 0,
            "count": 5,
            "srv_count": 4,
            "serror_rate": 0.02,
            "srv_serror_rate": 0.02,
            "rerror_rate": 0.01,
            "srv_rerror_rate": 0.01,
            "same_srv_rate": 0.95,
            "same_ctry_rate": 0.98,
            "dst_host_count": 10,
            "dst_host_srv_count": 8,
            "dst_host_same_srv_rate": 0.9,
            "dst_host_diff_srv_rate": 0.1,
            "dst_host_same_src_port_rate": 0.95,
            "dst_host_srv_diff_host_rate": 0.05,
            "dst_host_serror_rate": 0.01,
            "dst_host_srv_serror_rate": 0.01,
            "dst_host_rerror_rate": 0.01,
            "dst_host_srv_rerror_rate": 0.01
        }
    }

@app.get("/classes", tags=["info"])
async def get_classes():
    """Get available traffic classes"""
    if not model_loaded or metadata is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    return {
        "classes": metadata['classes'],
        "count": len(metadata['classes'])
    }

if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "="*60)
    print("🚀 STARTING FASTAPI SERVER")
    print("="*60)
    print("\n📍 API will be available at: http://localhost:8000")
    print("📚 Swagger Docs: http://localhost:8000/docs")
    print("🔄 ReDoc: http://localhost:8000/redoc")
    print("\n" + "="*60 + "\n")
    
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
