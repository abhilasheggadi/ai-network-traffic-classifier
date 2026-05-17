# 🔒 AI Network Traffic Classifier

**Smart Machine Learning-based Network Traffic Classification & Real-time Threat Detection**

An intelligent system that analyzes network traffic patterns and automatically classifies them as normal or malicious using a trained Random Forest machine learning model. Features a beautiful Streamlit dashboard for visualization and a production-ready FastAPI backend for predictions.

**Status:** ✅ Production Ready | 🚀 Fully Deployed | ✨ Beginner Friendly

---

## 📚 Table of Contents

- [What is This?](#-what-is-this)
- [Features](#-features)
- [Quick Start](#-quick-start-2-minutes)
- [Installation](#-installation-detailed)
- [Running the Application](#-running-the-application)
- [Docker Deployment](#-docker-deployment-production)
- [API Usage](#-api-usage)
- [Project Structure](#-project-structure)
- [Troubleshooting](#-troubleshooting)
- [For Developers](#-for-developers)

---

## 🤔 What is This?

This project uses **Machine Learning** to analyze network traffic and detect malicious activity. Think of it as a security guard that watches network traffic 24/7 and alerts you if something suspicious is happening.

**In simple terms:**
- 📊 **Input:** Network traffic data (source IP, ports, data rate, etc.)
- 🧠 **Processing:** ML model analyzes patterns
- 📤 **Output:** Classification (Normal ✅ or Malicious ⚠️)

**Real-world use cases:**
- 🛡️ Detect network attacks and intrusions
- 📈 Monitor unusual data patterns
- ⚠️ Alert security teams of threats
- 📊 Generate reports for compliance

---

## ✨ Features

### 🎨 **User-Friendly Dashboard**
- 6-page Streamlit interface
- Real-time traffic visualization
- Interactive charts and analytics
- Live prediction interface
- Performance metrics & statistics
- Alert system for suspicious traffic

### 🔌 **Production-Ready API**
- FastAPI backend with OpenAPI documentation
- Authentication via API keys
- Input validation & error handling
- Health check endpoints
- Structured logging for debugging
- CORS security configured

### 🧠 **ML Model**
- Random Forest classifier (pre-trained)
- High accuracy on network traffic data
- Fast inference (milliseconds)
- NSL-KDD dataset trained
- Model versioning & metadata

### 🐳 **Docker Support**
- Containerized deployment
- Docker Compose orchestration
- Multi-stage builds (optimized images)
- Health checks & auto-restart
- Production-ready configuration

### 🛡️ **Security**
- API key authentication
- Input validation
- CORS protection
- Audit logging
- Non-root Docker user

---

## 🎯 Quick Start (2 Minutes)

### Option 1: With Docker (Recommended)

**Requirements:** Docker & Docker Compose installed

```bash
# 1. Clone the repository
git clone https://github.com/GulrezQayyum/Networking.git
cd Networking

# 2. Start services
docker-compose up -d

# 3. Open in browser
# Dashboard: http://localhost:8501
# API Docs: http://localhost:8000/docs
```

### Option 2: Local Installation

**Requirements:** Python 3.9+

```bash
# 1. Clone repository
git clone https://github.com/GulrezQayyum/Networking.git
cd Networking

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start backend API
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000

# 5. In another terminal, start dashboard
streamlit run src/dashboard/app.py

# 6. Open browser
# Dashboard: http://localhost:8501
# API: http://localhost:8000
```

---

## 📦 Installation (Detailed)

### Prerequisites

Before you start, make sure you have:

- **Git** - For cloning the repository
  ```bash
  # Check if installed
  git --version
  ```

- **Docker & Docker Compose** (Option 1)
  ```bash
  # Install from: https://www.docker.com/products/docker-desktop
  docker --version
  docker-compose --version
  ```

- **Python 3.9+** (Option 2)
  ```bash
  # Check version
  python --version
  ```

### Step-by-Step Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/GulrezQayyum/Networking.git
cd Networking
```

#### 2. Set Up Environment Variables (Optional)

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` for your configuration (optional for development):

```bash
API_KEY=your-secure-key-here
CORS_ORIGINS=http://localhost:8501
```

#### 3a. Docker Installation (Recommended)

```bash
# Start all services in Docker
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f backend
```

#### 3b. Local Installation

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -c "import fastapi, streamlit; print('✅ Ready!')"
```

---

## 🚀 Running the Application

### Option 1: Docker (Recommended for Beginners)

```bash
# Start everything
docker-compose up -d

# Stop everything
docker-compose down

# View logs
docker-compose logs -f

# Restart a service
docker-compose restart backend
```

### Option 2: Local Python

```bash
# Terminal 1: Start backend API
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000

# Terminal 2: Start dashboard
streamlit run src/dashboard/app.py

# Terminal 3: (Optional) Run tests
pytest
```

### Access the Application

After starting:

- 🎨 **Dashboard:** http://localhost:8501
- 🔌 **API:** http://localhost:8000
- 📚 **API Docs:** http://localhost:8000/docs (Interactive!)
- 🏥 **Health Check:** http://localhost:8000/health

---

## 🐳 Docker Deployment (Production)

### What is Docker?

Think of Docker as a box 📦 that contains your entire application with all dependencies. No matter where you run it (your computer, server, cloud), it works the same way.

### Why Use Docker?

✅ **Consistency** - Works on any machine
✅ **Isolation** - Doesn't affect system settings
✅ **Easy Deployment** - One command to start
✅ **Production-Ready** - Industry standard

### Docker Compose Explained

`docker-compose.yml` orchestrates two services:

1. **Backend API** (Port 8000)
   - FastAPI server
   - Handles predictions
   - Auto-restarts on failure

2. **Dashboard** (Port 8501)
   - Streamlit UI
   - Connects to backend
   - Real-time updates

### Deployment on Server

```bash
# SSH into your server
ssh user@your-server.com

# Clone repository
git clone https://github.com/GulrezQayyum/Networking.git
cd Networking

# Create .env with production settings
cat > .env << EOF
API_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(32))")
CORS_ORIGINS=https://yourdomain.com
LOG_LEVEL=INFO
DEMO_MODE=False
EOF

# Start services
docker-compose up -d

# View logs
docker-compose logs -f
```

---

## 📡 API Usage

### What is an API?

An API (Application Programming Interface) is how programs talk to each other. You send data to the API, it processes it, and returns results.

### Using the API

#### 1. **Interactive Documentation** (Easiest)

Visit: http://localhost:8000/docs

Try it out directly in your browser!

#### 2. **Python Example**

```python
import requests

# Define headers with API key
headers = {"X-API-Key": "dev-key-change-in-production"}

# Network traffic data to classify
traffic_data = {
    "duration": 120,
    "src_bytes": 1024,
    "dst_bytes": 2048,
    "count": 10,
    "srv_count": 5,
    "dst_host_count": 3
}

# Make prediction request
response = requests.post(
    "http://localhost:8000/predict",
    json=traffic_data,
    headers=headers
)

# Get result
result = response.json()
print(f"Classification: {result['classification']}")
print(f"Confidence: {result['confidence']:.2%}")
```

#### 3. **cURL Example** (Command Line)

```bash
curl -X POST http://localhost:8000/predict \
  -H "X-API-Key: dev-key-change-in-production" \
  -H "Content-Type: application/json" \
  -d '{
    "duration": 120,
    "src_bytes": 1024,
    "dst_bytes": 2048,
    "count": 10,
    "srv_count": 5,
    "dst_host_count": 3
  }'
```

### API Endpoints

| Endpoint | Method | Purpose | Auth |
|----------|--------|---------|------|
| `/health` | GET | Check if API is running | ❌ |
| `/predict` | POST | Classify network traffic | ✅ |
| `/docs` | GET | Interactive documentation | ❌ |
| `/redoc` | GET | Alternative documentation | ❌ |

---

## 📁 Project Structure

```
Networking/
├── backend/
│   └── main.py                    # FastAPI application
├── src/
│   └── dashboard/
│       └── app.py                 # Streamlit dashboard (6 pages)
├── model/
│   ├── train.py                   # Train ML model
│   ├── inspect_model.py            # Inspect model details
│   └── saved_models/
│       ├── traffic_classifier.pkl  # Trained model
│       ├── scaler.pkl              # Feature scaler
│       ├── label_encoder.pkl       # Label encoder
│       └── metadata.json           # Model metadata
├── dataset/
│   ├── download_nsl_kdd.py        # Download dataset
│   └── generate_synthetic.py       # Generate test data
├── tests/
│   ├── test_api.py                # API tests
│   └── test_model.py              # Model tests
├── config.py                       # Configuration
├── requirements.txt                # Dependencies
├── docker-compose.yml              # Docker orchestration
├── Dockerfile                      # Container definition
├── DEPLOYMENT.md                   # Deployment guide
├── SETUP.md                        # Setup guide
└── README.md                       # This file
```

### Key Files Explained

| File | Purpose |
|------|---------|
| `config.py` | Centralized configuration (paths, keys, settings) |
| `.env` | Environment variables (local, not committed) |
| `docker-compose.yml` | Multi-container Docker setup |
| `requirements.txt` | Python package dependencies |
| `DEPLOYMENT.md` | Detailed deployment instructions |
| `SETUP.md` | Step-by-step setup guide |

---

## 🔧 Troubleshooting

### Issue: "Connection refused" on localhost

**Solution:**
```bash
# Check if services are running
docker-compose ps

# If not running, start them
docker-compose up -d

# Check logs for errors
docker-compose logs backend
```

### Issue: "Port already in use"

**Solution:**
```bash
# Find what's using the port
lsof -i :8000  # Check port 8000

# Or use a different port in docker-compose.yml
# Change: "8000:8000" to "8001:8000"
```

### Issue: "ModuleNotFoundError" or import errors

**Solution:**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Or in Docker
docker-compose down
docker-compose up -d --build
```

### Issue: Model not found

**Solution:**
```bash
# Check if model files exist
ls -la model/saved_models/

# If missing, train a new model
python model/train.py

# Check logs for details
cat logs/prediction.log
```

### Issue: API Key authentication fails

**Solution:**
```bash
# In your request, make sure you include the header
headers = {"X-API-Key": "dev-key-change-in-production"}

# Or check what key is set in config
grep API_KEY config.py
```

### Issue: Dashboard can't reach API

**Solution (Docker):**
```bash
# Make sure both containers are on same network
docker-compose ps

# Restart services
docker-compose restart
```

**Solution (Local):**
```bash
# Start backend first
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000

# Then start dashboard in another terminal
streamlit run src/dashboard/app.py
```

---

## 👨‍💻 For Developers

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=backend --cov=src

# Run specific test file
pytest tests/test_api.py -v

# Run specific test
pytest tests/test_api.py::test_health_check -v
```

### Training a New Model

```bash
# Generate synthetic training data
python dataset/generate_synthetic.py

# Train model
python model/train.py

# Inspect model
python model/inspect_model.py
```

### Development Workflow

```bash
# 1. Create feature branch
git checkout -b feature/your-feature

# 2. Make changes and test
pytest

# 3. Commit changes
git add .
git commit -m "Add your feature"

# 4. Push to GitHub
git push origin feature/your-feature

# 5. Create Pull Request on GitHub
```

### Code Structure Best Practices

- **config.py** - All configuration in one place
- **backend/main.py** - API endpoints and routes
- **src/dashboard/app.py** - Dashboard UI logic
- **model/train.py** - ML model training
- **tests/** - All tests here
- **logs/** - Application logs (auto-generated)

### Performance Tips

1. **Use Docker** for consistent performance
2. **Enable caching** in Streamlit dashboard
3. **Batch predictions** for multiple records
4. **Monitor logs** for bottlenecks
5. **Use Health Check** endpoint regularly

---

## 📄 Important Files

- **[SETUP.md](SETUP.md)** - Detailed setup instructions
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Deployment & production guide
- **[config.py](config.py)** - Configuration reference
- **[.env.example](.env.example)** - Environment variables template

---

## 🤝 Contributing

Found a bug? Have an idea? Contributions welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`pytest`)
5. Commit (`git commit -m 'Add amazing feature'`)
6. Push (`git push origin feature/amazing-feature`)
7. Open a Pull Request

---

## 📜 License

This project is open source and available under the MIT License.

---

## ❓ FAQ

**Q: Can I use this for production?**
A: Yes! It's production-ready with security, logging, and Docker support.

**Q: What's the accuracy of the model?**
A: Check `model/saved_models/metadata.json` for model performance metrics.

**Q: How do I change the API port?**
A: Edit `docker-compose.yml` or `.env` file: `API_PORT=9000`

**Q: Can I train with my own data?**
A: Yes! Edit `model/train.py` and point to your dataset.

**Q: Is the API key really necessary?**
A: For production yes, for development you can leave it as default.

---

## 📞 Support

- 📖 Read **SETUP.md** for setup issues
- 🐛 Check **[Troubleshooting](#-troubleshooting)** section
- 🐳 For Docker issues, see **DEPLOYMENT.md**
- 📝 Review API docs at http://localhost:8000/docs

---

**Made with ❤️ for Network Security**

Happy analyzing! 🚀
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


