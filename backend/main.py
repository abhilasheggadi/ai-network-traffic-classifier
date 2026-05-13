"""
FastAPI Backend - Network Traffic Classifier
Prediction API for the trained model
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import numpy as np
from datetime import datetime
from pathlib import Path
import json
import sys

# Add project root to path for config imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import (
    MODEL_PATH, SCALER_PATH, ENCODER_PATH, METADATA_PATH,
    CORS_ORIGINS, CORS_CREDENTIALS, CORS_METHODS, CORS_HEADERS,
    TRAFFIC_CLASSES
)

# Initialize FastAPI app
app = FastAPI(
    title="AI Network Traffic Classifier",
    description="ML-powered network traffic classification API",
    version="1.0.0"
)

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
    """Request model for traffic prediction"""
    duration: float
    protocol_type: str
    service: str
    flag: str
    src_bytes: float
    dst_bytes: float
    land: int
    wrong_fragment: int
    urgent: int
    hot: int
    num_failed_logins: int
    logged_in: int
    num_compromised: int
    root_shell: int
    su_attempted: int
    num_root: int
    num_file_creations: int
    num_shells: int
    num_access_files: int
    num_outbound_cmds: int
    is_host_login: int
    is_guest_login: int
    count: int
    srv_count: int
    serror_rate: float
    srv_serror_rate: float
    rerror_rate: float
    srv_rerror_rate: float
    same_srv_rate: float
    same_ctry_rate: float
    dst_host_count: int
    dst_host_srv_count: int
    dst_host_same_srv_rate: float
    dst_host_diff_srv_rate: float
    dst_host_same_src_port_rate: float
    dst_host_srv_diff_host_rate: float
    dst_host_serror_rate: float
    dst_host_srv_serror_rate: float
    dst_host_rerror_rate: float
    dst_host_srv_rerror_rate: float

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
async def predict(request: PredictionRequest):
    """
    Predict traffic classification
    
    Returns the predicted traffic type and confidence score
    """
    
    if not model_loaded or model is None:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Please check server logs."
        )
    
    try:
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
        
        return PredictionResponse(
            prediction=prediction_label,
            confidence=confidence,
            timestamp=datetime.utcnow().isoformat(),
            probabilities=proba_dict
        )
        
    except Exception as e:
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
