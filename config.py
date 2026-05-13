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

API_HOST = os.getenv("API_HOST", "127.0.0.1")
API_PORT = int(os.getenv("API_PORT", "8000"))
API_RELOAD = os.getenv("API_RELOAD", "True").lower() == "true"
API_LOG_LEVEL = os.getenv("API_LOG_LEVEL", "error")

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
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# ============================================================================
# DATABASE SETTINGS (Optional)
# ============================================================================

DB_URL = os.getenv("DB_URL", f"sqlite:///{DATA_DIR}/app.db")
USE_DATABASE = os.getenv("USE_DATABASE", "False").lower() == "true"

# ============================================================================
# CORS SETTINGS
# ============================================================================

CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
CORS_CREDENTIALS = os.getenv("CORS_CREDENTIALS", "True").lower() == "true"
CORS_METHODS = os.getenv("CORS_METHODS", "*").split(",")
CORS_HEADERS = os.getenv("CORS_HEADERS", "*").split(",")

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
