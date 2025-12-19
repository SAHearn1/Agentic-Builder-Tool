"""
Vercel serverless function entry point.
This is the handler that Vercel will invoke.
"""
import sys
import os

# Add the parent directory to Python path so imports work
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

try:
    from src.main import app

    # Vercel will look for this variable
    handler = app

except Exception as e:
    # If import fails, create a minimal error-reporting app
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse

    error_app = FastAPI()

    @error_app.get("/")
    @error_app.get("/{path:path}")
    async def catch_all(path: str = ""):
        return JSONResponse(
            status_code=500,
            content={
                "error": "Application failed to initialize",
                "details": str(e),
                "path": path
            }
        )

    handler = error_app
