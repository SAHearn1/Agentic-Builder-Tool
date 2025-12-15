"""Unit tests for data models."""

from src.models import AgentResponse, HealthResponse, TaskRequest


def test_task_request():
    """Test TaskRequest model."""
    request = TaskRequest(task="Deploy a website")

    assert request.task == "Deploy a website"
    assert request.context is None
    assert request.max_iterations is None


def test_task_request_with_context():
    """Test TaskRequest with all fields."""
    request = TaskRequest(
        task="Deploy a website",
        context="Use React",
        max_iterations=5,
    )

    assert request.task == "Deploy a website"
    assert request.context == "Use React"
    assert request.max_iterations == 5


def test_health_response():
    """Test HealthResponse model."""
    response = HealthResponse(status="healthy", version="0.1.0")

    assert response.status == "healthy"
    assert response.version == "0.1.0"


def test_agent_response():
    """Test AgentResponse model."""
    response = AgentResponse(
        success=True,
        message="Task completed",
        artifacts=["https://example.com"],
        metadata={"duration": 10.5},
    )

    assert response.success is True
    assert response.message == "Task completed"
    assert response.artifacts == ["https://example.com"]
    assert response.metadata["duration"] == 10.5
