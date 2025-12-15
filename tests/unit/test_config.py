"""Unit tests for configuration module."""

import pytest
from pydantic import ValidationError

from src.config import Settings


def test_settings_validation():
    """Test that Settings requires mandatory fields."""
    with pytest.raises(ValidationError):
        Settings()


def test_settings_with_env_vars(monkeypatch):
    """Test Settings with environment variables."""
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test_key")
    monkeypatch.setenv("GITHUB_TOKEN", "test_token")
    monkeypatch.setenv("VERCEL_TOKEN", "test_vercel")
    monkeypatch.setenv("GCS_PROJECT_ID", "test_project")
    monkeypatch.setenv("GCS_BUCKET_NAME", "test_bucket")

    settings = Settings()

    assert settings.anthropic_api_key == "test_key"
    assert settings.github_token == "test_token"
    assert settings.vercel_token == "test_vercel"
    assert settings.gcs_project_id == "test_project"
    assert settings.gcs_bucket_name == "test_bucket"
    assert settings.app_env == "development"
    assert settings.agent_model == "claude-3-5-sonnet-20241022"
