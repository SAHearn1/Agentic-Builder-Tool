"""Request models for API endpoints."""

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class TaskRequest(BaseModel):
    """Request model for agent task execution."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "task": "Create a new React app and deploy it to Vercel",
                "context": "Use TypeScript and Tailwind CSS",
                "max_iterations": 10,
            }
        }
    )

    task: str = Field(..., description="Description of the DevOps task to perform")
    context: Optional[str] = Field(None, description="Additional context for the task")
    max_iterations: Optional[int] = Field(None, description="Override max iterations")


class AgentRequest(BaseModel):
    """General request model for agent interactions."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": "List all my GitHub repositories",
                "session_id": "session-123",
            }
        }
    )

    message: str = Field(..., description="Message to send to the agent")
    session_id: Optional[str] = Field(None, description="Session ID for conversation continuity")
