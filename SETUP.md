# 🚀 Setup Guide - AI Network Traffic Classifier

Complete setup instructions for running the AI Network Traffic Classifier locally.

## 📋 Prerequisites

- **Python 3.9+** (Check: `python --version`)
- **pip** (Python package manager)
- **Git** (for cloning the repo)

---

## 🔧 Step 1: Clone & Setup Project

### 1.1 Clone the Repository
```bash
git clone https://github.com/GulrezQayyum/Networking.git
cd Networking
```

### 1.2 Create Virtual Environment
```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

**Verify activation:**
```bash
which python  # macOS/Linux
# Output should show: /path/to/venv/bin/python

python --version  # Should show 3.9 or higher
```

---

## 📦 Step 2: Install Dependencies

### 2.1 Update pip
```bash
pip install --upgrade pip
```

### 2.2 Install Project Requirements
```bash
pip install -r requirements.txt
```

**Verify installation:**
```bash
pip list | grep streamlit
pip list | grep fastapi
# Should see both packages listed
```

### 2.3 (Optional) Create `.env` File
```bash
# Copy the example file
cp .env.example .env

# Edit if needed (most defaults are fine for demo)
# nano .env  # or use your editor
```

---

## 🤖 Step 3: Verify/Train Model

The trained model files should already exist:

```bash
ls -la model/saved_models/
```

**Should see:**
- `traffic_classifier.pkl` (3.5 MB)
- `scaler.pkl` (1.3 KB)
- `label_encoder.pkl` (508 B)
- `metadata.json` (658 B)

**If missing, train the model:**
```bash
python model/train.py
```

---

## 🖥️ Step 4: Start Services

### Option A: Run Services Separately (Recommended for Development)

**Terminal 1 - Start FastAPI Backend:**
```bash
source venv/bin/activate  # Activate if not already
python -m uvicorn backend.main:app --reload --port 8000
```

**Expected output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
✅ Model loaded successfully!
```

**Terminal 2 - Start Streamlit Dashboard:**
```bash
source venv/bin/activate  # Activate if not already
python -m streamlit run src/dashboard/app.py --server.port 8501
```

**Expected output:**
```
  You can now view your Streamlit app in your browser.
  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

### Option B: Run Both with Single Command

```bash
# After activating venv
python -m uvicorn backend.main:app --reload --port 8000 &
python -m streamlit run src/dashboard/app.py --server.port 8501
```

---

## 🌐 Step 5: Access the Services

### Dashboard (Frontend)
```
http://localhost:8501
```

**Features:**
- 🎯 Dashboard - Traffic overview & metrics
- 📡 Live Traffic - Real-time packet stream
- 🎯 Predictions - Manual traffic classification
- 📊 Traffic Analysis - Advanced analytics
- 🤖 Model Performance - Model metrics
- ⚠️ Alerts - Security events

### API Endpoints (Backend)
```
http://127.0.0.1:8000
```

**Key endpoints:**
- `GET /` - API info
- `GET /health` - Health check
- `GET /docs` - Interactive API documentation (Swagger UI)
- `POST /predict` - Classify traffic
- `GET /info` - Model info
- `GET /features` - Feature list
- `GET /classes` - Traffic classes

---

## 🧪 Step 6: Test the System

### Test API Health
```bash
curl http://127.0.0.1:8000/health
```

**Expected response:**
```json
{
  "status": "online",
  "model_loaded": true,
  "version": "1.0.0"
}
```

### Test Prediction
```bash
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "duration": 120,
    "src_bytes": 5000,
    "dst_bytes": 4000,
    "count": 5,
    "srv_count": 4,
    "serror_rate": 0.02,
    "srv_serror_rate": 0.02,
    "rerror_rate": 0.01,
    "srv_rerror_rate": 0.01,
    "same_srv_rate": 0.95,
    "dst_host_count": 10,
    "dst_host_srv_count": 8,
    "protocol_type": "tcp",
    "service": "http",
    "flag": "S2",
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
    "same_ctry_rate": 0.98,
    "dst_host_same_srv_rate": 0.9,
    "dst_host_diff_srv_rate": 0.1,
    "dst_host_same_src_port_rate": 0.95,
    "dst_host_srv_diff_host_rate": 0.05,
    "dst_host_serror_rate": 0.01,
    "dst_host_srv_serror_rate": 0.01,
    "dst_host_rerror_rate": 0.01,
    "dst_host_srv_rerror_rate": 0.01
  }'
```

---

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'streamlit'"

**Solution:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows

# Reinstall
pip install streamlit plotly requests
```

### Issue: "Model files not found"

**Solution:**
```bash
# Check if files exist
ls -la model/saved_models/

# If missing, train the model
python model/train.py
```

### Issue: "Address already in use" (Port 8000 or 8501)

**Solution:**
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or use different ports
python -m uvicorn backend.main:app --port 8002
python -m streamlit run src/dashboard/app.py --server.port 8502
```

### Issue: "Connection refused" between Dashboard and API

**Solution:**
```bash
# Ensure API is running
curl http://127.0.0.1:8000/health

# Check config in src/dashboard/app.py
# Make sure API_BASE_URL = "http://127.0.0.1:8000"
```

---

## 📁 Project Structure

```
Networking/
├── backend/
│   └── main.py              # FastAPI server
├── model/
│   ├── train.py             # Model training script
│   ├── inspect_model.py      # Model inspection
│   └── saved_models/         # Trained model files
├── src/
│   └── dashboard/
│       └── app.py            # Streamlit dashboard
├── data/                     # Data outputs
├── dataset/                  # Datasets
├── config.py                 # Configuration
├── requirements.txt          # Python dependencies
├── .env.example              # Environment template
└── README.md                 # Project documentation
```

---

## 🚀 Deployment Options

### Local Development
```bash
source venv/bin/activate
python -m uvicorn backend.main:app --reload
# In another terminal:
python -m streamlit run src/dashboard/app.py
```

### Production (with Gunicorn)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 backend.main:app
```

### Docker (Future)
```bash
docker-compose up
```

---

## ✅ Verification Checklist

- [ ] Virtual environment created and activated
- [ ] All packages installed (`pip list` shows streamlit, fastapi, etc.)
- [ ] Model files exist in `model/saved_models/`
- [ ] FastAPI running on port 8000
- [ ] Streamlit running on port 8501
- [ ] Dashboard loads at `http://localhost:8501`
- [ ] API health check returns 200 status
- [ ] Prediction test returns classification

---

## 📞 Support & Issues

**Model Repository:**
https://github.com/GulrezQayyum/network-traffic-classifier-model

**Common Issues:**
- See Troubleshooting section above
- Check `.env` configuration
- Verify all dependencies installed

---

## 🎉 You're All Set!

Your AI Network Traffic Classifier is now running! 

**Next Steps:**
1. Open http://localhost:8501 in your browser
2. Explore the Dashboard page
3. Try making predictions
4. Check Model Performance metrics
5. Review Alerts and Live Traffic

Happy analyzing! 🔒
