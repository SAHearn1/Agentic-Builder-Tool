"""
Vercel diagnostic endpoint to check configuration.
Access at /api/diagnostic to see what's configured.
"""
import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
@app.get("/api/diagnostic")
async def diagnostic():
    """Show configuration status without revealing secrets."""

    env_vars = {
        "ANTHROPIC_API_KEY": bool(os.getenv("ANTHROPIC_API_KEY")),
        "GITHUB_TOKEN": bool(os.getenv("GITHUB_TOKEN")),
        "VERCEL_TOKEN": bool(os.getenv("VERCEL_TOKEN")),
        "GCS_PROJECT_ID": bool(os.getenv("GCS_PROJECT_ID")),
        "GCS_BUCKET_NAME": bool(os.getenv("GCS_BUCKET_NAME")),
        "GOOGLE_APPLICATION_CREDENTIALS_JSON": bool(os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON")),
        "APP_ENV": os.getenv("APP_ENV", "not set"),
        "APP_PORT": os.getenv("APP_PORT", "not set"),
        "PYTHONPATH": os.getenv("PYTHONPATH", "not set"),
    }

    import sys

    return {
        "status": "diagnostic",
        "environment_variables": env_vars,
        "python_version": sys.version,
        "python_path": sys.path[:5],  # First 5 entries
        "cwd": os.getcwd(),
        "message": "Check if all environment variables are set to True"
    }

handler = app
