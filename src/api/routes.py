"""API routes for the agent service."""

import logging
from typing import Dict

from fastapi import APIRouter, HTTPException
from langchain_core.messages import HumanMessage

from src import __version__
from src.agent import create_agent_graph
from src.models import AgentResponse, HealthResponse, TaskRequest

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint.

    Returns:
        Service health status
    """
    return HealthResponse(status="healthy", version=__version__)


@router.post("/agent/task", response_model=AgentResponse)
async def execute_task(request: TaskRequest) -> AgentResponse:
    """Execute a DevOps task using the autonomous agent.

    Args:
        request: Task request with description and parameters

    Returns:
        Agent execution result
    """
    try:
        logger.info(f"Executing task: {request.task}")

        # Create agent graph
        agent = create_agent_graph()

        # Prepare initial state
        task_description = request.task
        if request.context:
            task_description += f"\n\nContext: {request.context}"

        initial_state = {
            "messages": [HumanMessage(content=task_description)],
            "task": request.task,
            "code_generated": "",
            "deployment_status": "pending",
            "artifacts": [],
            "iteration_count": 0,
        }

        # Execute agent
        result = agent.invoke(initial_state)

        # Extract response
        final_message = result["messages"][-1].content if result["messages"] else "No response"

        return AgentResponse(
            success=True,
            message=final_message,
            artifacts=result.get("artifacts", []),
            metadata={
                "iterations": result.get("iteration_count", 0),
                "deployment_status": result.get("deployment_status", "unknown"),
            },
        )
    except Exception as e:
        logger.error(f"Error executing task: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Task execution failed: {str(e)}")


@router.get("/agent/status")
async def get_status() -> Dict[str, str]:
    """Get agent status and configuration.

    Returns:
        Agent status information
    """
    return {
        "status": "ready",
        "version": __version__,
        "description": "Autonomous DevOps Agent",
    }
