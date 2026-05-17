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
git clone https://github.com/GulrezQayyum/network-traffic-classifier-model.git
cd network-traffic-classifier-model
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

---

## 🧪 Step 6: Troubleshooting

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
# Check if both services are running
# Terminal 1: Backend should show "Uvicorn running on http://127.0.0.1:8000"
# Terminal 2: Streamlit should show "You can now view your Streamlit app"

# Restart both services
# Kill both processes and start again
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
