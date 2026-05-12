# AI Network Traffic Classifier

Machine learning-based network traffic classification using NSL-KDD dataset.

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
