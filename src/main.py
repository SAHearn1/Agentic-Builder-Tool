"""Main FastAPI application with LangServe integration."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langserve import add_routes

from src import __version__
from src.agent import create_agent_graph
from src.api import router
from src.config import get_settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    logger.info("Starting Agentic Tool Builder application...")
    settings = get_settings()
    logger.info(f"Environment: {settings.app_env}")
    logger.info(f"Agent model: {settings.agent_model}")
    yield
    logger.info("Shutting down Agentic Tool Builder application...")


# Create FastAPI app
app = FastAPI(
    title="Agentic Tool Builder",
    description="Autonomous DevOps Agent using LangGraph, FastAPI, and Cloud Tools",
    version=__version__,
    lifespan=lifespan,
)

# Add CORS middleware
# For production, set ALLOWED_ORIGINS env var to specific domains
# Never use allow_credentials=True with allow_origins=["*"] in production
import os
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,  # Changed to False for security when using wildcard origins
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, tags=["agent"])

# Add LangServe routes for the agent
try:
    agent_graph = create_agent_graph()
    add_routes(
        app,
        agent_graph,
        path="/agent",
        enabled_endpoints=["invoke", "stream"],
    )
    logger.info("LangServe routes added successfully")
except Exception as e:
    logger.warning(f"Could not add LangServe routes: {e}")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "Agentic Tool Builder",
        "version": __version__,
        "description": "Autonomous DevOps Agent",
        "endpoints": {
            "health": "/health",
            "status": "/agent/status",
            "task": "/agent/task",
            "langserve": "/agent/invoke (POST), /agent/stream (POST)",
        },
    }


if __name__ == "__main__":
    import uvicorn

    settings = get_settings()
    uvicorn.run(
        "src.main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=settings.app_env == "development",
    )
