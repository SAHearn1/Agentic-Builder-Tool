"""Tools module for DevOps operations."""

from .github_tools import github_tools
from .vercel_tools import vercel_tools
from .gcs_tools import gcs_tools


def get_all_tools():
    """Get all available tools for the agent.
    
    Returns:
        List of all tool instances
    """
    return [
        *github_tools,
        *vercel_tools,
        *gcs_tools,
    ]


__all__ = ["get_all_tools", "github_tools", "vercel_tools", "gcs_tools"]
