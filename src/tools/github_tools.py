"""GitHub tools for repository and code management."""

from typing import Optional

from github import Github, GithubException
from langchain_core.tools import tool

from src.config import get_settings

# Default limit for repository listings
DEFAULT_REPO_LIMIT = 10


@tool
def create_github_repo(repo_name: str, description: str = "", private: bool = False) -> str:
    """Create a new GitHub repository.

    Args:
        repo_name: Name of the repository to create
        description: Repository description
        private: Whether the repository should be private

    Returns:
        Repository URL and creation status
    """
    settings = get_settings()
    gh = Github(settings.github_token)

    try:
        user = gh.get_user()
        repo = user.create_repo(
            name=repo_name,
            description=description,
            private=private,
            auto_init=True,
        )
        return f"Successfully created repository: {repo.html_url}"
    except GithubException as e:
        return f"Error creating repository: {str(e)}"


@tool
def commit_file_to_github(
    repo_name: str,
    file_path: str,
    file_content: str,
    commit_message: str,
    branch: str = "main",
) -> str:
    """Commit a file to a GitHub repository.

    Args:
        repo_name: Repository name (format: owner/repo)
        file_path: Path where the file should be stored in the repo
        file_content: Content of the file
        commit_message: Commit message
        branch: Branch name (default: main)

    Returns:
        Commit status and SHA
    """
    settings = get_settings()
    gh = Github(settings.github_token)

    try:
        repo = gh.get_repo(repo_name)

        # Check if file exists
        try:
            existing_file = repo.get_contents(file_path, ref=branch)
            # Update existing file
            result = repo.update_file(
                path=file_path,
                message=commit_message,
                content=file_content,
                sha=existing_file.sha,
                branch=branch,
            )
            return f"Successfully updated file: {file_path}. Commit SHA: {result['commit'].sha}"
        except GithubException:
            # Create new file
            result = repo.create_file(
                path=file_path,
                message=commit_message,
                content=file_content,
                branch=branch,
            )
            return f"Successfully created file: {file_path}. Commit SHA: {result['commit'].sha}"
    except GithubException as e:
        return f"Error committing file: {str(e)}"


@tool
def create_pull_request(
    repo_name: str,
    title: str,
    body: str,
    head_branch: str,
    base_branch: str = "main",
) -> str:
    """Create a pull request in a GitHub repository.

    Args:
        repo_name: Repository name (format: owner/repo)
        title: Pull request title
        body: Pull request description
        head_branch: Source branch
        base_branch: Target branch (default: main)

    Returns:
        Pull request URL and status
    """
    settings = get_settings()
    gh = Github(settings.github_token)

    try:
        repo = gh.get_repo(repo_name)
        pr = repo.create_pull(
            title=title,
            body=body,
            head=head_branch,
            base=base_branch,
        )
        return f"Successfully created pull request: {pr.html_url}"
    except GithubException as e:
        return f"Error creating pull request: {str(e)}"


@tool
def list_github_repos(org_name: Optional[str] = None) -> str:
    """List GitHub repositories for a user or organization.

    Args:
        org_name: Organization name (optional, defaults to authenticated user)

    Returns:
        List of repositories
    """
    settings = get_settings()
    gh = Github(settings.github_token)

    try:
        if org_name:
            entity = gh.get_organization(org_name)
        else:
            entity = gh.get_user()

        repos = entity.get_repos()
        repo_list = [
            f"{repo.full_name} - {repo.description or 'No description'}" for repo in repos[:10]
        ]  # Limit to 10 repos
        return "Repositories:\n" + "\n".join(repo_list)
    except GithubException as e:
        return f"Error listing repositories: {str(e)}"


# Export tools list
github_tools = [
    create_github_repo,
    commit_file_to_github,
    create_pull_request,
    list_github_repos,
]
