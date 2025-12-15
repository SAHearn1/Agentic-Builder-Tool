"""
FastAPI server for DevOps-Builder agent.
Exposes the LangGraph agent via LangServe endpoints.
"""
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langserve import add_routes
from agent import agent_graph

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="DevOps-Builder Agent API",
    description="An autonomous DevOps engineer powered by Claude 3.5 Sonnet and LangGraph",
    version="1.0.0",
)

# Add CORS middleware for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "DevOps-Builder Agent",
        "version": "1.0.0",
        "endpoints": {
            "agent": "/agent",
            "playground": "/agent/playground",
            "docs": "/docs"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "ok"}


# Add LangServe routes for the agent
# This exposes the agent at /agent with playground at /agent/playground
add_routes(
    app,
    agent_graph,
    path="/agent",
    enabled_endpoints=["invoke", "batch", "stream", "playground"],
)


if __name__ == "__main__":
    import uvicorn
    
    # Get port from environment variable or default to 8080
    port = int(os.getenv("PORT", "8080"))
    
    print(f"🚀 Starting DevOps-Builder Agent server on port {port}...")
    print(f"📝 API docs available at http://0.0.0.0:{port}/docs")
    print(f"🎮 Agent playground available at http://0.0.0.0:{port}/agent/playground")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
