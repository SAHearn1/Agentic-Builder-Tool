"""Response models for API endpoints."""

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field


class HealthResponse(BaseModel):
    """Health check response."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "healthy",
                "version": "0.1.0",
            }
        }
    )

    status: str = Field(..., description="Service status")
    version: str = Field(..., description="Application version")


class AgentResponse(BaseModel):
    """Response from agent task execution."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "message": "Successfully deployed application to Vercel",
                "artifacts": ["https://example.vercel.app"],
                "metadata": {"deployment_id": "dpl_123", "duration": 45.2},
            }
        }
    )

    success: bool = Field(..., description="Whether the task was successful")
    message: str = Field(..., description="Response message from the agent")
    artifacts: Optional[list[str]] = Field(None, description="Generated artifacts (URLs, etc.)")
    metadata: Optional[dict[str, Any]] = Field(None, description="Additional metadata")
