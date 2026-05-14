"""
API Tests for Network Traffic Classifier
Tests the FastAPI endpoints and authentication
"""

import pytest


class TestHealth:
    """Health endpoint tests"""
    
    def test_root_endpoint(self, client):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "online"
        assert data["version"] == "1.0.0"
    
    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "model_loaded" in data


class TestAuthentication:
    """API Key authentication tests"""
    
    def test_predict_without_api_key(self, client, valid_prediction_payload):
        """Test prediction without API key - should fail"""
        response = client.post("/predict", json=valid_prediction_payload)
        assert response.status_code == 403
        assert "Invalid or missing API key" in response.json()["detail"]
    
    def test_predict_with_invalid_api_key(self, client, valid_prediction_payload):
        """Test prediction with invalid API key - should fail"""
        headers = {"X-API-Key": "invalid-key"}
        response = client.post("/predict", json=valid_prediction_payload, headers=headers)
        assert response.status_code == 403
    
    def test_predict_with_valid_api_key(self, client, valid_prediction_payload, api_headers):
        """Test prediction with valid API key - should succeed"""
        response = client.post("/predict", json=valid_prediction_payload, headers=api_headers)
        assert response.status_code == 200
        data = response.json()
        assert "prediction" in data
        assert "confidence" in data


class TestPredictions:
    """Prediction endpoint tests"""
    
    def test_valid_prediction(self, client, valid_prediction_payload, api_headers):
        """Test valid prediction request"""
        response = client.post("/predict", json=valid_prediction_payload, headers=api_headers)
        assert response.status_code == 200
        data = response.json()
        
        # Validate response structure
        assert "prediction" in data
        assert "confidence" in data
        assert "timestamp" in data
        assert "probabilities" in data
        
        # Validate values
        assert isinstance(data["prediction"], str)
        assert 0 <= data["confidence"] <= 1
        assert isinstance(data["probabilities"], dict)
    
    def test_invalid_duration_negative(self, client, valid_prediction_payload, api_headers):
        """Test with invalid negative duration"""
        valid_prediction_payload["duration"] = -10
        response = client.post("/predict", json=valid_prediction_payload, headers=api_headers)
        assert response.status_code == 422  # Validation error
    
    def test_invalid_duration_too_large(self, client, valid_prediction_payload, api_headers):
        """Test with duration exceeding max"""
        valid_prediction_payload["duration"] = 100000
        response = client.post("/predict", json=valid_prediction_payload, headers=api_headers)
        assert response.status_code == 422
    
    def test_invalid_serror_rate_out_of_range(self, client, valid_prediction_payload, api_headers):
        """Test with invalid error rate"""
        valid_prediction_payload["serror_rate"] = 1.5
        response = client.post("/predict", json=valid_prediction_payload, headers=api_headers)
        assert response.status_code == 422
    
    def test_missing_required_field(self, client, api_headers):
        """Test with missing required field"""
        incomplete_payload = {"duration": 120}
        response = client.post("/predict", json=incomplete_payload, headers=api_headers)
        assert response.status_code == 422
    
    def test_prediction_consistency(self, client, valid_prediction_payload, api_headers):
        """Test that same input produces same output"""
        response1 = client.post("/predict", json=valid_prediction_payload, headers=api_headers)
        response2 = client.post("/predict", json=valid_prediction_payload, headers=api_headers)
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        data1 = response1.json()
        data2 = response2.json()
        
        # Same input should produce same prediction
        assert data1["prediction"] == data2["prediction"]
        assert abs(data1["confidence"] - data2["confidence"]) < 0.001


class TestInfo:
    """Info endpoints tests"""
    
    def test_get_info(self, client):
        """Test model info endpoint"""
        response = client.get("/info")
        assert response.status_code == 200
        data = response.json()
        assert "features" in data
        assert "classes" in data
        assert "metrics" in data
    
    def test_get_features(self, client):
        """Test features endpoint"""
        response = client.get("/features")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "required_features" in data
        assert isinstance(data["required_features"], list)
        assert len(data["required_features"]) > 0
        assert data["count"] == len(data["required_features"])
