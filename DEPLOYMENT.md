# 🚀 Deployment Guide - AI Network Traffic Classifier

Complete guide for deploying the AI Network Traffic Classifier using Docker.

---

## 📋 Prerequisites

- **Docker** 20.10+ ([Install Docker](https://docs.docker.com/get-docker/))
- **Docker Compose** 2.0+ (usually comes with Docker Desktop)
- **Git** (for cloning the repo)

Verify installation:
```bash
docker --version
docker-compose --version
```

---

## 🔐 Security Improvements

This version includes the following production-ready improvements:

### 1. **Authentication** ✅
- API Key authentication on all prediction endpoints
- Default development key: `dev-key-change-in-production`
- Configure via `API_KEY` environment variable

### 2. **Input Validation** ✅
- Strict type validation on all request fields
- Range validation for numeric inputs (e.g., 0-1 for rates)
- Automatic rejection of invalid data
- Clear error messages for debugging

### 3. **CORS Security** ✅
- Removed wildcard CORS (*) for security
- Only allows localhost by default
- Configurable via `CORS_ORIGINS` environment variable

### 4. **Logging & Monitoring** ✅
- Structured logging with rotating file handlers
- Separate logs for API and predictions (audit trail)
- JSON-formatted logs available for analysis
- Automatic log rotation (10MB per file, 5 backups)

### 5. **Testing** ✅
- Comprehensive unit and integration tests
- API authentication tests
- Input validation tests
- Model consistency tests
- Run tests with: `pytest`

---

## 🐳 Docker Deployment

### Quick Start (Recommended)

1. **Clone the repository**
```bash
git clone https://github.com/GulrezQayyum/Networking.git
cd Networking
```

2. **Create environment file (optional)**
```bash
# Copy example if it exists
cp .env.example .env

# Or create your own with production settings
cat > .env << EOF
API_KEY=your-secure-api-key-here
CORS_ORIGINS=http://yourdomain.com,http://yourapp.com
LOG_LEVEL=INFO
API_LOG_LEVEL=info
DEMO_MODE=False
EOF
```

3. **Start services with Docker Compose**
```bash
docker-compose up -d
```

4. **Check service status**
```bash
docker-compose ps
docker-compose logs -f
```

5. **Access services**
- **Dashboard:** http://localhost:8501
- **API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## 🔑 API Key Management

### For Development
Default key is fine for local testing:
```bash
API_KEY=dev-key-change-in-production
```

### For Production
**MUST change the API key!**

```bash
# Generate a secure key
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Set in .env or docker-compose
echo "API_KEY=your-generated-key-here" > .env
```

### Using API Key in Requests

**Via curl:**
```bash
curl -X POST http://localhost:8000/predict \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"duration": 120, ...}'
```

**Via Python:**
```python
import requests

headers = {"X-API-Key": "your-api-key"}
response = requests.post(
    "http://localhost:8000/predict",
    json=payload,
    headers=headers
)
```

**Via Dashboard:**
- API key is configured in `src/dashboard/app.py`
- Line 139: `API_KEY = "dev-key-change-in-production"`
- Update this for production

---

## 📊 Docker Commands

### Start Services
```bash
# Start in foreground (see logs)
docker-compose up

# Start in background
docker-compose up -d

# Start with fresh rebuild
docker-compose up --build
```

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f dashboard

# Last N lines
docker-compose logs --tail=50
```

### Stop Services
```bash
# Graceful stop
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Stop specific service
docker-compose stop backend
```

### Restart Services
```bash
# Restart all
docker-compose restart

# Restart specific
docker-compose restart backend
```

### Build Images
```bash
# Build without starting
docker-compose build

# Build specific service
docker-compose build backend

# Build with no cache
docker-compose build --no-cache
```

---

## 🧪 Running Tests

### In Docker Container
```bash
# Run all tests
docker-compose exec backend pytest

# Run with coverage
docker-compose exec backend pytest --cov=.

# Run specific test file
docker-compose exec backend pytest tests/test_api.py

# Run specific test
docker-compose exec backend pytest tests/test_api.py::TestHealth::test_root_endpoint

# Verbose output
docker-compose exec backend pytest -v
```

### Locally (without Docker)
```bash
# Install test dependencies
pip install -r requirements.txt

# Run tests
pytest

# With coverage
pytest --cov=.

# Generate HTML report
pytest --cov=. --cov-report=html
# Open htmlcov/index.html in browser
```

---

## 📁 File Volumes

Docker Compose mounts local directories for persistence:

| Local Path | Container Path | Purpose |
|-----------|-----------------|---------|
| `./logs` | `/app/logs` | Application logs |
| `./data` | `/app/data` | Data storage |
| `./model/saved_models` | `/app/model/saved_models` | ML models |
| `./src/dashboard` | `/app/src/dashboard` | Dashboard code (live reload) |

**Logs are automatically persisted** - accessible at `./logs/`

---

## 🔍 Monitoring & Health Checks

### API Health Check
```bash
curl http://localhost:8000/health
# Response: {"status":"online","model_loaded":true,"version":"1.0.0"}
```

### Dashboard Health Check
```bash
curl http://localhost:8501/_stcore/health
```

### Docker Health Status
```bash
docker-compose ps
# Look for "healthy" status
```

### View Metrics
Check log files for audit trails:
```bash
# API logs
tail -f logs/api.log

# Prediction logs (audit trail)
tail -f logs/predictions.log
```

---

## 🚨 Troubleshooting

### Backend won't start
```bash
# Check logs
docker-compose logs backend

# Verify model files exist
ls -la model/saved_models/

# Rebuild image
docker-compose down
docker-compose build --no-cache
docker-compose up backend
```

### Dashboard can't connect to API
```bash
# Check API is running
docker-compose ps backend
docker-compose logs backend

# Check API is healthy
docker-compose exec backend curl http://localhost:8000/health

# Verify API key matches in dashboard
grep API_KEY src/dashboard/app.py
echo $API_KEY
```

### Permission Denied Errors
```bash
# Ensure logs directory is writable
chmod 755 logs/
mkdir -p logs
```

### Port Already in Use
```bash
# Change ports in docker-compose.yml
# Or kill process using port:
lsof -i :8000  # See what's using port 8000
kill -9 <PID>
```

---

## 📈 Production Checklist

Before deploying to production:

- [ ] Change `API_KEY` to a secure random value
- [ ] Update `CORS_ORIGINS` to your domain
- [ ] Set `DEMO_MODE=False` if using real data
- [ ] Configure external reverse proxy (nginx/Traefik)
- [ ] Set up SSL/TLS certificates
- [ ] Configure logging centralization (ELK, Splunk, etc.)
- [ ] Set up monitoring and alerts
- [ ] Configure automatic backups for `./data`
- [ ] Test database persistence
- [ ] Review security settings in `config.py`
- [ ] Run full test suite: `pytest`
- [ ] Load test the API endpoints

---

## 🔄 Kubernetes Deployment (Advanced)

For Kubernetes deployment:

1. **Build and push image to registry**
```bash
docker build -t your-registry/network-classifier:1.0 .
docker push your-registry/network-classifier:1.0
```

2. **Create Kubernetes manifests** (example structure):
```yaml
# backend-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: network-classifier-api
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: api
        image: your-registry/network-classifier:1.0
        ports:
        - containerPort: 8000
        env:
        - name: API_KEY
          valueFrom:
            secretKeyRef:
              name: api-secrets
              key: api-key
```

3. **Deploy**
```bash
kubectl apply -f k8s/
```

---

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Streamlit Deployment](https://docs.streamlit.io/library/deploy)

---

## 📞 Support

For issues or questions:
1. Check logs: `docker-compose logs -f`
2. Review this guide's Troubleshooting section
3. Check GitHub issues
4. Contact the development team

---

**Version:** 1.0.0  
**Last Updated:** May 14, 2026
