"""Integration tests for API endpoints."""

from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint."""
    response = client.get("/")

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Agentic Tool Builder"
    assert "version" in data
    assert "endpoints" in data


def test_health_endpoint():
    """Test health check endpoint."""
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data


def test_status_endpoint():
    """Test agent status endpoint."""
    response = client.get("/agent/status")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ready"
    assert "version" in data
    assert "description" in data
