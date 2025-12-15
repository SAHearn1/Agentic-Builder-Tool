"""Application settings and configuration."""

from functools import lru_cache
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Anthropic Configuration
    anthropic_api_key: str = Field(..., description="Anthropic API key")
    
    # GitHub Configuration
    github_token: str = Field(..., description="GitHub personal access token")
    github_default_org: Optional[str] = Field(None, description="Default GitHub organization")
    
    # Vercel Configuration
    vercel_token: str = Field(..., description="Vercel API token")
    vercel_team_id: Optional[str] = Field(None, description="Vercel team ID (optional)")
    
    # Google Cloud Storage Configuration
    gcs_project_id: str = Field(..., description="GCP project ID")
    gcs_bucket_name: str = Field(..., description="GCS bucket name")
    google_application_credentials: Optional[str] = Field(
        None, description="Path to GCP service account key"
    )
    
    # Application Configuration
    app_env: str = Field(default="development", description="Application environment")
    app_host: str = Field(default="0.0.0.0", description="Application host")
    app_port: int = Field(default=8000, description="Application port")
    log_level: str = Field(default="INFO", description="Log level")
    
    # Agent Configuration
    agent_model: str = Field(
        default="claude-3-5-sonnet-20241022", description="Claude model to use"
    )
    agent_temperature: float = Field(default=0.7, description="Agent temperature")
    agent_max_iterations: int = Field(default=10, description="Maximum agent iterations")


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
