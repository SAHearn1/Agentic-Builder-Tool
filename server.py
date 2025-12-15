"""
FastAPI server for DevOps-Builder agent.
Exposes the LangGraph agent via LangServe endpoints.
"""
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request
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
# For production, set ALLOWED_ORIGINS to specific domains (e.g., "https://app.example.com,https://dashboard.example.com")
# Never use allow_credentials=True with allow_origins=["*"] in production
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
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


@app.post("/webhook")
async def github_webhook(request: Request):
    """
    GitHub webhook endpoint for automated DevOps workflows.
    Triggered when code is pushed to a GitHub repository.
    """
    # Parse the data sent by GitHub
    payload = await request.json()
    
    # Extract useful info
    try:
        repo_name = payload['repository']['full_name']
        branch = payload['ref'].replace('refs/heads/', '')
        commit_msg = payload['head_commit']['message']
        sender = payload['sender']['login']
    except KeyError:
        return {"status": "ignored", "reason": "Not a push event"}

    # Construct a prompt for the Agent
    mission = f"""
    EVENT_TRIGGER: New code pushed by {sender}.
    REPO: {repo_name}
    BRANCH: {branch}
    COMMIT_MESSAGE: "{commit_msg}"
    
    ACTION REQUIRED: 
    1. Pull the latest code from this branch.
    2. Analyze the changes for errors.
    3. If healthy, trigger a deployment.
    """

    # Wake up the Agent (Invoke the Graph directly)
    # We run this in the background so GitHub gets a fast "200 OK" response
    config = {"configurable": {"thread_id": f"webhook-{payload['head_commit']['id']}"}}
    
    # Note: In a real production app, use BackgroundTasks here. 
    # For now, we await it to keep it simple.
    result = await agent_graph.ainvoke(
        {"messages": [("user", mission)]}, 
        config=config
    )

    return {"status": "success", "agent_response": "Workflow started"}


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
