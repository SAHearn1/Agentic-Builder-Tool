"""
Tools for the DevOps-Builder agent.
Includes GitHub integration, Vercel deployment, and GCS logging.
"""
import os
from typing import Optional
from datetime import datetime
import httpx
from langchain_core.tools import tool
from langchain_community.agent_toolkits.github.toolkit import GitHubToolkit
from langchain_community.utilities.github import GitHubAPIWrapper
from google.cloud import storage


def get_tools():
    """
    Returns a list of tools for the DevOps-Builder agent.
    Includes GitHub toolkit and custom Vercel/GCS tools.
    """
    tools = []
    
    # GitHub Toolkit
    github_token = os.getenv("GITHUB_ACCESS_TOKEN")
    if github_token:
        try:
            github = GitHubAPIWrapper(github_access_token=github_token)
            github_toolkit = GitHubToolkit.from_github_api_wrapper(github)
            tools.extend(github_toolkit.get_tools())
        except Exception as e:
            print(f"Warning: Could not initialize GitHub toolkit: {e}")
    else:
        print("Warning: GITHUB_ACCESS_TOKEN not set, GitHub tools will not be available")
    
    # Add custom tools
    tools.append(trigger_vercel_deployment)
    tools.append(log_build_status)
    
    return tools


@tool
def trigger_vercel_deployment(
    project_name: str,
    git_source: Optional[str] = None,
    environment: str = "production"
) -> str:
    """
    Triggers a deployment on Vercel for the specified project.
    
    Args:
        project_name: The name of the Vercel project to deploy
        git_source: Optional git branch or commit to deploy
        environment: The deployment environment (production, preview, or development)
    
    Returns:
        A message indicating the deployment status with deployment URL
    """
    vercel_token = os.getenv("VERCEL_TOKEN")
    
    if not vercel_token:
        return "Error: VERCEL_TOKEN environment variable is not set"
    
    # Vercel API endpoint for deployments
    url = "https://api.vercel.com/v13/deployments"
    
    # Prepare headers with authorization
    headers = {
        "Authorization": f"Bearer {vercel_token}",
        "Content-Type": "application/json"
    }
    
    # Prepare deployment payload
    payload = {
        "name": project_name,
        "target": environment
    }
    
    if git_source:
        payload["gitSource"] = {
            "type": "github",
            "ref": git_source
        }
    
    try:
        # Make the API request
        with httpx.Client(timeout=30.0) as client:
            response = client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            
            result = response.json()
            deployment_url = result.get("url", "N/A")
            deployment_id = result.get("id", "N/A")
            
            return (
                f"✅ Vercel deployment triggered successfully!\n"
                f"Project: {project_name}\n"
                f"Environment: {environment}\n"
                f"Deployment ID: {deployment_id}\n"
                f"URL: https://{deployment_url}"
            )
    
    except httpx.HTTPStatusError as e:
        return f"Error: Vercel API request failed with status {e.response.status_code}: {e.response.text}"
    except Exception as e:
        return f"Error triggering Vercel deployment: {str(e)}"


@tool
def log_build_status(
    build_name: str,
    status: str,
    details: Optional[str] = None
) -> str:
    """
    Logs build status information to Google Cloud Storage.
    
    Args:
        build_name: The name/identifier of the build
        status: The build status (e.g., 'success', 'failure', 'in_progress')
        details: Optional additional details about the build
    
    Returns:
        A message indicating whether the log was successfully written
    """
    bucket_name = os.getenv("GCS_BUCKET_NAME")
    
    if not bucket_name:
        return "Error: GCS_BUCKET_NAME environment variable is not set"
    
    try:
        # Initialize GCS client
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        
        # Create log entry
        timestamp = datetime.utcnow().isoformat()
        log_content = f"""Build Log Entry
==================
Build Name: {build_name}
Status: {status}
Timestamp: {timestamp}
Details: {details or 'N/A'}
"""
        
        # Create blob name with timestamp
        blob_name = f"build-logs/{build_name}/{timestamp.replace(':', '-')}.txt"
        blob = bucket.blob(blob_name)
        
        # Upload log to GCS
        blob.upload_from_string(log_content, content_type="text/plain")
        
        return (
            f"✅ Build status logged successfully to GCS!\n"
            f"Bucket: {bucket_name}\n"
            f"Path: {blob_name}\n"
            f"Status: {status}"
        )
    
    except Exception as e:
        return f"Error logging build status to GCS: {str(e)}"
