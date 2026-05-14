"""
Configuration settings for AI Network Traffic Classifier
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ============================================================================
# PROJECT PATHS
# ============================================================================

PROJECT_ROOT = Path(__file__).parent
MODEL_DIR = PROJECT_ROOT / "model" / "saved_models"
DATA_DIR = PROJECT_ROOT / "data"
LOGS_DIR = PROJECT_ROOT / "logs"

# Create directories if they don't exist
DATA_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# ============================================================================
# API SETTINGS
# ============================================================================

API_HOST = os.getenv("API_HOST", "0.0.0.0")  # Changed to 0.0.0.0 for Docker
API_PORT = int(os.getenv("API_PORT", "8000"))
API_RELOAD = os.getenv("API_RELOAD", "True").lower() == "true"
API_LOG_LEVEL = os.getenv("API_LOG_LEVEL", "info")

# ============================================================================
# DASHBOARD SETTINGS
# ============================================================================

DASHBOARD_PORT = int(os.getenv("DASHBOARD_PORT", "8501"))
DASHBOARD_HOST = os.getenv("DASHBOARD_HOST", "localhost")

# ============================================================================
# MODEL SETTINGS
# ============================================================================

MODEL_NAME = "traffic_classifier.pkl"
SCALER_NAME = "scaler.pkl"
ENCODER_NAME = "label_encoder.pkl"
METADATA_NAME = "metadata.json"

# Model files paths
MODEL_PATH = MODEL_DIR / MODEL_NAME
SCALER_PATH = MODEL_DIR / SCALER_NAME
ENCODER_PATH = MODEL_DIR / ENCODER_NAME
METADATA_PATH = MODEL_DIR / METADATA_NAME

# ============================================================================
# FEATURE SETTINGS
# ============================================================================

FEATURES = [
    "duration", "src_bytes", "dst_bytes", "count", "srv_count",
    "serror_rate", "srv_serror_rate", "rerror_rate", "srv_rerror_rate",
    "same_srv_rate", "dst_host_count", "dst_host_srv_count"
]

TRAFFIC_CLASSES = ["dos", "normal", "probe", "r2l", "u2r"]

# ============================================================================
# LOGGING SETTINGS
# ============================================================================

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = LOGS_DIR / "traffic_classifier.log"
LOG_API_FILE = LOGS_DIR / "api.log"
LOG_PREDICTIONS_FILE = LOGS_DIR / "predictions.log"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_JSON_FORMAT = '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "logger": "%(name)s", "message": "%(message)s"}'

# ============================================================================
# DATABASE SETTINGS (Optional)
# ============================================================================

DB_URL = os.getenv("DB_URL", f"sqlite:///{DATA_DIR}/app.db")
USE_DATABASE = os.getenv("USE_DATABASE", "False").lower() == "true"

# ============================================================================
# CORS SETTINGS
# ============================================================================

# Default origins - only localhost for development
DEFAULT_CORS_ORIGINS = [
    "http://localhost:8501",
    "http://127.0.0.1:8501",
    "http://localhost:3000",  # For future React frontend
    "http://127.0.0.1:3000"
]

# Get from environment, use defaults if not specified (more secure)
CORS_ORIGINS = os.getenv("CORS_ORIGINS", ",".join(DEFAULT_CORS_ORIGINS)).split(",")
CORS_ORIGINS = [origin.strip() for origin in CORS_ORIGINS]
CORS_CREDENTIALS = os.getenv("CORS_CREDENTIALS", "True").lower() == "true"
CORS_METHODS = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
CORS_HEADERS = ["Content-Type", "Authorization"]

# ============================================================================
# SECURITY SETTINGS
# ============================================================================

# API Key for authentication
API_KEY = os.getenv("API_KEY", "dev-key-change-in-production")
API_KEY_HEADER = "X-API-Key"

# Allowed traffic classes for validation
ALLOWED_TRAFFIC_CLASSES = ["dos", "normal", "probe", "r2l", "u2r"]

# Feature validation ranges (min, max)
FEATURE_RANGES = {
    "duration": (0, 86400),  # 0 to 24 hours
    "src_bytes": (0, 10000000),  # 0 to 10 MB
    "dst_bytes": (0, 10000000),
    "count": (1, 511),
    "srv_count": (1, 511),
    "serror_rate": (0.0, 1.0),
    "srv_serror_rate": (0.0, 1.0),
    "rerror_rate": (0.0, 1.0),
    "srv_rerror_rate": (0.0, 1.0),
    "same_srv_rate": (0.0, 1.0),
    "dst_host_count": (1, 255),
    "dst_host_srv_count": (1, 255),
}

# ============================================================================
# DEMO MODE (Synthetic Data)
# ============================================================================

DEMO_MODE = os.getenv("DEMO_MODE", "True").lower() == "true"

# ============================================================================
# VALIDATION
# ============================================================================

def validate_config():
    """Validate that all required files exist"""
    missing_files = []
    
    required_files = [
        (MODEL_PATH, "Model"),
        (SCALER_PATH, "Scaler"),
        (ENCODER_PATH, "Encoder"),
        (METADATA_PATH, "Metadata"),
    ]
    
    for path, name in required_files:
        if not path.exists():
            missing_files.append(f"{name} ({path})")
    
    if missing_files:
        print(f"⚠️  Warning: Missing files: {', '.join(missing_files)}")
        return False
    
    return True

# Validate on import
if not validate_config():
    print("⚠️  Some model files are missing. Train the model first:")
    print("   python model/train.py")
