"""
Pytest configuration and fixtures for AI Network Traffic Classifier
"""

import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    # TestClient triggers startup/shutdown events by default
    with TestClient(app) as client:
        yield client


@pytest.fixture
def valid_prediction_payload():
    """Valid prediction request payload"""
    return {
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


@pytest.fixture
def api_headers():
    """API headers with valid API key"""
    return {"X-API-Key": "dev-key-change-in-production"}
