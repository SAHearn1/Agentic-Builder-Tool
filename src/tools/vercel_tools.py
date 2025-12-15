"""Vercel tools for deployment operations."""

import httpx
from langchain_core.tools import tool

from src.config import get_settings


def _get_vercel_headers():
    """Get headers for Vercel API requests."""
    settings = get_settings()
    headers = {
        "Authorization": f"Bearer {settings.vercel_token}",
        "Content-Type": "application/json",
    }
    if settings.vercel_team_id:
        headers["X-Vercel-Team-Id"] = settings.vercel_team_id
    return headers


@tool
def create_vercel_project(project_name: str, framework: str = "other") -> str:
    """Create a new Vercel project.
    
    Args:
        project_name: Name of the project to create
        framework: Framework type (nextjs, vite, other, etc.)
        
    Returns:
        Project creation status and ID
    """
    try:
        headers = _get_vercel_headers()
        
        payload = {
            "name": project_name,
            "framework": framework,
        }
        
        with httpx.Client() as client:
            response = client.post(
                "https://api.vercel.com/v10/projects",
                headers=headers,
                json=payload,
                timeout=30.0,
            )
            
            if response.status_code == 200:
                data = response.json()
                return f"Successfully created Vercel project: {project_name}. ID: {data.get('id')}"
            else:
                return f"Error creating project: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Error creating Vercel project: {str(e)}"


@tool
def deploy_to_vercel(project_name: str, git_repo_url: str, branch: str = "main") -> str:
    """Deploy a GitHub repository to Vercel.
    
    Args:
        project_name: Vercel project name
        git_repo_url: GitHub repository URL
        branch: Git branch to deploy (default: main)
        
    Returns:
        Deployment status and URL
    """
    try:
        headers = _get_vercel_headers()
        
        payload = {
            "name": project_name,
            "gitSource": {
                "type": "github",
                "repo": git_repo_url,
                "ref": branch,
            },
        }
        
        with httpx.Client() as client:
            response = client.post(
                "https://api.vercel.com/v13/deployments",
                headers=headers,
                json=payload,
                timeout=60.0,
            )
            
            if response.status_code in [200, 201]:
                data = response.json()
                deployment_url = data.get("url", "")
                return f"Successfully deployed to Vercel. URL: https://{deployment_url}"
            else:
                return f"Error deploying: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Error deploying to Vercel: {str(e)}"


@tool
def list_vercel_deployments(project_name: str, limit: int = 5) -> str:
    """List recent deployments for a Vercel project.
    
    Args:
        project_name: Vercel project name
        limit: Number of deployments to return (default: 5)
        
    Returns:
        List of recent deployments
    """
    try:
        headers = _get_vercel_headers()
        
        with httpx.Client() as client:
            response = client.get(
                f"https://api.vercel.com/v6/deployments?projectId={project_name}&limit={limit}",
                headers=headers,
                timeout=30.0,
            )
            
            if response.status_code == 200:
                data = response.json()
                deployments = data.get("deployments", [])
                
                if not deployments:
                    return "No deployments found."
                
                deployment_list = []
                for d in deployments[:limit]:
                    deployment_list.append(
                        f"- {d.get('url')} (State: {d.get('state')}, Created: {d.get('created')})"
                    )
                
                return f"Recent deployments:\n" + "\n".join(deployment_list)
            else:
                return f"Error listing deployments: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Error listing Vercel deployments: {str(e)}"


@tool
def get_vercel_project_info(project_name: str) -> str:
    """Get information about a Vercel project.
    
    Args:
        project_name: Vercel project name or ID
        
    Returns:
        Project information
    """
    try:
        headers = _get_vercel_headers()
        
        with httpx.Client() as client:
            response = client.get(
                f"https://api.vercel.com/v9/projects/{project_name}",
                headers=headers,
                timeout=30.0,
            )
            
            if response.status_code == 200:
                data = response.json()
                return (
                    f"Project: {data.get('name')}\n"
                    f"ID: {data.get('id')}\n"
                    f"Framework: {data.get('framework')}\n"
                    f"Production URL: {data.get('targets', {}).get('production', {}).get('url')}"
                )
            else:
                return f"Error getting project info: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Error getting Vercel project info: {str(e)}"


# Export tools list
vercel_tools = [
    create_vercel_project,
    deploy_to_vercel,
    list_vercel_deployments,
    get_vercel_project_info,
]
