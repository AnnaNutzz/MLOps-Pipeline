from fastapi.testclient import TestClient
import pytest
from app.main import app

client = TestClient(app)

def test_health_check():
    """
    Test the health check endpoint.
    """
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_predict_success():
    """
    Test the prediction endpoint with valid data.
    """
    # Example data with 8 features
    valid_data = {
        "data": [
            [5.0, 121.0, 72.0, 23.0, 112.0, 26.2, 0.245, 30.0],
            [1.0, 126.0, 60.0, 0.0, 0.0, 30.1, 0.349, 47.0]
        ]
    }
    response = client.post("/predict", json=valid_data)
    assert response.status_code == 200
    json_response = response.json()
    assert "predictions" in json_response
    assert isinstance(json_response["predictions"], list)
    assert len(json_response["predictions"]) == 2

def test_predict_invalid_shape():
    """
    Test the prediction endpoint with malformed data (incorrect number of features).
    """
    # Data with only 7 features
    invalid_data = {
        "data": [
            [5.0, 121.0, 72.0, 23.0, 112.0, 26.2, 0.245]
        ]
    }
    response = client.post("/predict", json=invalid_data)
    assert response.status_code == 400
    assert "detail" in response.json()
    assert "Expected 8 features" in response.json()["detail"]

def test_predict_empty_data():
    """
    Test the prediction endpoint with an empty data list.
    """
    response = client.post("/predict", json={"data": []})
    assert response.status_code == 200
    assert response.json() == {"predictions": []} 