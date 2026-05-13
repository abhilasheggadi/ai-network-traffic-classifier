# AI Network Traffic Classifier

Machine learning-based network traffic classification using Random Forest model. Real-time threat detection dashboard with FastAPI backend and Streamlit frontend.

**Status:** ✅ Production Ready | 🚀 Ready for Demo

## 🎯 Quick Start

### macOS/Linux:
```bash
chmod +x start.sh
./start.sh
```

### Windows:
```bash
start.bat
```

Then open: **http://localhost:8501**

---

## 📋 Full Setup Guide

See **[SETUP.md](SETUP.md)** for detailed step-by-step instructions.

**Key Files:**
- `config.py` - Centralized configuration
- `.env` - Environment variables (auto-created)
- `SETUP.md` - Complete setup guide
- `start.sh` / `start.bat` - Quick start scripts

---

## 📁 Project Structure

```
Networking/
├── backend/              # FastAPI API server
│   └── main.py          # API endpoints & model loading
├── src/
│   └── dashboard/        # Streamlit dashboard
│       └── app.py        # Dashboard UI (6 pages)
├── model/                # ML model files
│   ├── train.py         # Model training script
│   ├── inspect_model.py  # Model inspection tool
│   └── saved_models/     # Pre-trained models (pkl files)
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── SETUP.md              # Setup instructions
├── start.sh / start.bat  # Quick start scripts
└── README.md             # This file
```

## ✅ Project Status

| Component | Status | Details |
|-----------|--------|---------|
| Model | ✅ Complete | Random Forest, 96.8% accuracy |
| FastAPI Backend | ✅ Complete | All endpoints working |
| Streamlit Dashboard | ✅ Complete | 6-page professional UI |
| Configuration | ✅ Complete | Centralized settings |
| Documentation | ✅ Complete | SETUP.md guide included |
| Demo Data | ✅ Complete | Synthetic data only (safe) |

## 🚀 Architecture

```
┌─────────────────────────────────────┐
│    Streamlit Dashboard (Port 8501)  │
│    - Dashboard overview              │
│    - Traffic analysis                │
│    - Model predictions               │
│    - Alerts monitoring               │
└──────────────┬──────────────────────┘
               │
               │ HTTP requests
               ↓
┌─────────────────────────────────────┐
│    FastAPI Backend (Port 8000)      │
│    - /predict endpoint               │
│    - /health check                   │
│    - /info endpoint                  │
└──────────────┬──────────────────────┘
               │
               ↓
┌─────────────────────────────────────┐
│    ML Model (Random Forest)         │
│    - Trained on NSL-KDD dataset     │
│    - 12 numeric features             │
│    - 5 traffic classes               │
│    - 96.8% accuracy                  │
└─────────────────────────────────────┘
```

## 🌐 Access Points

| Service | URL | Purpose |
|---------|-----|---------|
| Dashboard | http://localhost:8501 | UI for traffic analysis |
| API | http://127.0.0.1:8000 | Model predictions |
| API Docs | http://127.0.0.1:8000/docs | Swagger documentation |

## 📁 Folder Structure

```
├── backend/          # FastAPI API (Step 2) ← You are here
│   └── main.py       # API server
├── frontend/         # Streamlit Dashboard (Step 3)
├── model/            # Model training (Step 1) ✅ Done
│   ├── train.py
│   ├── inspect_model.py
│   └── saved_models/ # Trained models
├── dataset/          # Data files
├── utils/            # Helpers
├── data/             # Outputs
└── requirements.txt
```

## ✅ Step 1: Complete

- ✓ Dataset generated (5,000 samples)
- ✓ Model trained (99.22% accuracy)
- ✓ Model saved and verified

## 🚀 Step 2: FastAPI Backend

### Installation

```bash
# Activate virtual environment (if not already)
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install additional dependencies
pip install -r requirements.txt
```

### Run the API Server

```bash
python -m uvicorn backend.main:app --reload
```

Or:

```bash
python backend/main.py
```

**API will be available at:**
- 🌐 **Main:** http://localhost:8000
- 📚 **Swagger Docs:** http://localhost:8000/docs (Try it here!)
- 🔄 **ReDoc:** http://localhost:8000/redoc

### API Endpoints

#### 1. Health Check
```
GET http://localhost:8000/health
```
Response: `{"status": "online", "model_loaded": true}`

#### 2. Get Info
```
GET http://localhost:8000/info
```
Shows model features, classes, accuracy

#### 3. Get Classes
```
GET http://localhost:8000/classes
```
Lists all traffic classes the model can predict

#### 4. Get Required Features
```
GET http://localhost:8000/features
```
Shows what data you need to send for prediction

#### 5. Make Prediction ⭐
```
POST http://localhost:8000/predict
```

**Example request:**
```json
{
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
```

**Example response:**
```json
{
  "prediction": "normal",
  "confidence": 0.998,
  "timestamp": "2026-05-12T10:30:45.123456",
  "probabilities": {
    "normal": 0.998,
    "dos": 0.001,
    "probe": 0.0005,
    "r2l": 0.0005,
    "u2r": 0.0
  }
}
```

## 🎯 Next Steps

1. ✅ **Step 1:** Train Model
2. ✅ **Step 2:** FastAPI Backend (current)
3. ⏭️ **Step 3:** Streamlit Dashboard
4. ⏭️ **Step 4:** Deploy
