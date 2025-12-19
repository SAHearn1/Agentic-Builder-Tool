#!/usr/bin/env python3
"""
Environment Configuration Verification Script
Verifies that all required credentials and services are properly configured.
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# Color codes for terminal output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"


def print_header(text: str):
    """Print a formatted header."""
    print(f"\n{BLUE}{'=' * 70}{RESET}")
    print(f"{BLUE}{text:^70}{RESET}")
    print(f"{BLUE}{'=' * 70}{RESET}\n")


def print_success(text: str):
    """Print success message."""
    print(f"{GREEN}✓ {text}{RESET}")


def print_error(text: str):
    """Print error message."""
    print(f"{RED}✗ {text}{RESET}")


def print_warning(text: str):
    """Print warning message."""
    print(f"{YELLOW}⚠ {text}{RESET}")


def print_info(text: str):
    """Print info message."""
    print(f"  {text}")


def check_env_file() -> bool:
    """Check if .env file exists."""
    print_header("Environment File Check")

    env_file = Path(".env")
    env_example = Path(".env.example")

    if env_file.exists():
        print_success(".env file found")
        print_info(f"Location: {env_file.absolute()}")
        return True
    else:
        print_error(".env file not found")
        if env_example.exists():
            print_info("Run: cp .env.example .env")
            print_info("Then edit .env with your actual credentials")
        return False


def check_gitignore() -> bool:
    """Check if sensitive files are in .gitignore."""
    print_header("Git Security Check")

    gitignore = Path(".gitignore")
    checks = []

    if gitignore.exists():
        content = gitignore.read_text()

        # Check for .env
        if ".env" in content or "*.env" in content:
            print_success(".env is gitignored")
            checks.append(True)
        else:
            print_error(".env is NOT in .gitignore - SECURITY RISK!")
            print_info("Run: echo '.env' >> .gitignore")
            checks.append(False)

        # Check for service account keys
        if "*.json" in content or "gcp-service-account-key.json" in content:
            print_success("Service account keys are gitignored")
            checks.append(True)
        else:
            print_warning("Service account key files may not be gitignored")
            print_info("Consider adding: *.json or gcp-service-account-key.json")
            checks.append(False)
    else:
        print_error(".gitignore not found")
        checks.append(False)

    return all(checks)


def check_env_vars() -> Dict[str, bool]:
    """Check if required environment variables are set."""
    print_header("Environment Variables Check")

    # Load .env file if it exists
    env_file = Path(".env")
    if env_file.exists():
        from dotenv import load_dotenv
        load_dotenv()
        print_info("Loaded variables from .env file")

    required_vars = {
        "ANTHROPIC_API_KEY": "Anthropic Claude API",
        "GITHUB_TOKEN": "GitHub Personal Access Token",
        "VERCEL_TOKEN": "Vercel API Token",
        "GCS_PROJECT_ID": "Google Cloud Project ID",
        "GCS_BUCKET_NAME": "Google Cloud Storage Bucket",
    }

    optional_vars = {
        "GOOGLE_APPLICATION_CREDENTIALS": "GCP Service Account Key Path",
        "GITHUB_DEFAULT_ORG": "Default GitHub Organization",
        "VERCEL_TEAM_ID": "Vercel Team ID",
        "AGENT_MODEL": "Claude Model Version",
        "ALLOWED_ORIGINS": "CORS Allowed Origins",
    }

    results = {}

    print("\nRequired Variables:")
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value and len(value) > 0:
            # Show first/last few characters for verification
            masked = f"{value[:8]}...{value[-4:]}" if len(value) > 12 else "***"
            print_success(f"{var}: Set ({masked})")
            results[var] = True
        else:
            print_error(f"{var}: NOT SET - {description}")
            results[var] = False

    print("\nOptional Variables:")
    for var, description in optional_vars.items():
        value = os.getenv(var)
        if value and len(value) > 0:
            if var == "GOOGLE_APPLICATION_CREDENTIALS":
                print_success(f"{var}: {value}")
            else:
                masked = f"{value[:8]}..." if len(value) > 8 else "***"
                print_success(f"{var}: Set ({masked})")
            results[var] = True
        else:
            print_warning(f"{var}: Not set - {description} (optional)")
            results[var] = False

    return results


def check_gcp_credentials() -> bool:
    """Check GCP service account key file."""
    print_header("Google Cloud Credentials Check")

    creds_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

    if not creds_path:
        print_warning("GOOGLE_APPLICATION_CREDENTIALS not set")
        print_info("Set this to the path of your service account key JSON file")
        return False

    creds_file = Path(creds_path)

    if not creds_file.exists():
        print_error(f"Service account key file not found: {creds_path}")
        print_info("Download your service account key from GCP Console")
        return False

    print_success(f"Service account key file found: {creds_path}")

    # Check file permissions
    stat_info = creds_file.stat()
    mode = oct(stat_info.st_mode)[-3:]

    if mode == "600":
        print_success(f"File permissions are secure: {mode}")
    else:
        print_warning(f"File permissions: {mode} (recommend 600)")
        print_info(f"Run: chmod 600 {creds_path}")

    # Try to parse JSON
    try:
        import json
        with open(creds_file) as f:
            data = json.load(f)

        if "private_key" in data and "client_email" in data:
            print_success("Service account key is valid JSON format")
            print_info(f"Service account: {data.get('client_email', 'unknown')}")
            return True
        else:
            print_error("Service account key is missing required fields")
            return False
    except json.JSONDecodeError:
        print_error("Service account key is not valid JSON")
        return False


def test_anthropic_connection() -> bool:
    """Test connection to Anthropic API."""
    print_header("Anthropic API Connection Test")

    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key:
        print_error("ANTHROPIC_API_KEY not set - skipping test")
        return False

    try:
        import httpx

        print_info("Testing API connection...")

        response = httpx.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": "claude-3-5-sonnet-20241022",
                "max_tokens": 10,
                "messages": [{"role": "user", "content": "Hi"}],
            },
            timeout=30.0,
        )

        if response.status_code == 200:
            print_success("Anthropic API connection successful")
            print_info(f"Model: claude-3-5-sonnet-20241022")
            return True
        elif response.status_code == 401:
            print_error("Authentication failed - check your API key")
            return False
        else:
            print_error(f"API request failed: {response.status_code}")
            print_info(f"Response: {response.text[:200]}")
            return False

    except ImportError:
        print_warning("httpx not installed - skipping connection test")
        return False
    except Exception as e:
        print_error(f"Connection test failed: {str(e)}")
        return False


def test_github_connection() -> bool:
    """Test connection to GitHub API."""
    print_header("GitHub API Connection Test")

    token = os.getenv("GITHUB_TOKEN")

    if not token:
        print_error("GITHUB_TOKEN not set - skipping test")
        return False

    try:
        import httpx

        print_info("Testing API connection...")

        response = httpx.get(
            "https://api.github.com/user",
            headers={"Authorization": f"Bearer {token}"},
            timeout=30.0,
        )

        if response.status_code == 200:
            data = response.json()
            print_success("GitHub API connection successful")
            print_info(f"Authenticated as: {data.get('login', 'unknown')}")
            print_info(f"Account type: {data.get('type', 'unknown')}")

            # Check scopes
            scopes = response.headers.get("x-oauth-scopes", "")
            if scopes:
                print_info(f"Token scopes: {scopes}")

            return True
        elif response.status_code == 401:
            print_error("Authentication failed - check your token")
            return False
        else:
            print_error(f"API request failed: {response.status_code}")
            return False

    except ImportError:
        print_warning("httpx not installed - skipping connection test")
        return False
    except Exception as e:
        print_error(f"Connection test failed: {str(e)}")
        return False


def test_vercel_connection() -> bool:
    """Test connection to Vercel API."""
    print_header("Vercel API Connection Test")

    token = os.getenv("VERCEL_TOKEN")

    if not token:
        print_error("VERCEL_TOKEN not set - skipping test")
        return False

    try:
        import httpx

        print_info("Testing API connection...")

        headers = {"Authorization": f"Bearer {token}"}
        team_id = os.getenv("VERCEL_TEAM_ID")
        if team_id:
            headers["X-Vercel-Team-Id"] = team_id

        response = httpx.get(
            "https://api.vercel.com/v2/user",
            headers=headers,
            timeout=30.0,
        )

        if response.status_code == 200:
            data = response.json()
            user_data = data.get("user", {})
            print_success("Vercel API connection successful")
            print_info(f"Username: {user_data.get('username', 'unknown')}")
            print_info(f"Email: {user_data.get('email', 'unknown')}")
            return True
        elif response.status_code == 401 or response.status_code == 403:
            print_error("Authentication failed - check your token")
            return False
        else:
            print_error(f"API request failed: {response.status_code}")
            return False

    except ImportError:
        print_warning("httpx not installed - skipping connection test")
        return False
    except Exception as e:
        print_error(f"Connection test failed: {str(e)}")
        return False


def test_gcs_connection() -> bool:
    """Test connection to Google Cloud Storage."""
    print_header("Google Cloud Storage Connection Test")

    bucket_name = os.getenv("GCS_BUCKET_NAME")
    project_id = os.getenv("GCS_PROJECT_ID")

    if not bucket_name:
        print_error("GCS_BUCKET_NAME not set - skipping test")
        return False

    if not project_id:
        print_error("GCS_PROJECT_ID not set - skipping test")
        return False

    try:
        from google.cloud import storage

        print_info("Testing GCS connection...")

        # Set credentials if provided
        creds_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        if creds_path:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = creds_path

        client = storage.Client(project=project_id)
        bucket = client.bucket(bucket_name)

        # Test bucket exists
        if bucket.exists():
            print_success(f"Bucket '{bucket_name}' is accessible")

            # Test write permission with a test file
            test_blob = bucket.blob("_verify_test.txt")
            test_blob.upload_from_string("test")
            print_success("Write permission verified")

            # Clean up test file
            test_blob.delete()
            print_success("Delete permission verified")

            return True
        else:
            print_error(f"Bucket '{bucket_name}' does not exist or is not accessible")
            print_info(f"Create bucket: gsutil mb gs://{bucket_name}")
            return False

    except ImportError:
        print_warning("google-cloud-storage not installed - skipping connection test")
        return False
    except Exception as e:
        print_error(f"Connection test failed: {str(e)}")
        print_info("Check your service account permissions")
        return False


def check_dependencies() -> bool:
    """Check if required dependencies are installed."""
    print_header("Dependencies Check")

    required = [
        ("fastapi", "FastAPI"),
        ("uvicorn", "Uvicorn"),
        ("langchain", "LangChain"),
        ("langgraph", "LangGraph"),
        ("langchain_anthropic", "LangChain Anthropic"),
        ("pydantic", "Pydantic"),
        ("httpx", "HTTPX"),
        ("python_dotenv", "Python Dotenv"),
    ]

    all_installed = True

    for module, name in required:
        try:
            __import__(module)
            print_success(f"{name} installed")
        except ImportError:
            print_error(f"{name} NOT installed")
            all_installed = False

    if not all_installed:
        print_info("\nInstall dependencies: pip install -e \".[dev]\"")

    return all_installed


def main():
    """Run all verification checks."""
    print(f"\n{BLUE}{'=' * 70}{RESET}")
    print(f"{BLUE}{'Agentic Builder Tool - Environment Verification':^70}{RESET}")
    print(f"{BLUE}{'=' * 70}{RESET}")

    results = []

    # Run all checks
    results.append(("Environment File", check_env_file()))
    results.append(("Git Security", check_gitignore()))

    env_vars = check_env_vars()
    all_required = all(env_vars.get(var, False) for var in [
        "ANTHROPIC_API_KEY", "GITHUB_TOKEN", "VERCEL_TOKEN",
        "GCS_PROJECT_ID", "GCS_BUCKET_NAME"
    ])
    results.append(("Environment Variables", all_required))

    results.append(("GCP Credentials", check_gcp_credentials()))
    results.append(("Dependencies", check_dependencies()))

    # Connection tests
    results.append(("Anthropic API", test_anthropic_connection()))
    results.append(("GitHub API", test_github_connection()))
    results.append(("Vercel API", test_vercel_connection()))
    results.append(("Google Cloud Storage", test_gcs_connection()))

    # Summary
    print_header("Verification Summary")

    passed = sum(1 for _, status in results if status)
    total = len(results)

    for name, status in results:
        if status:
            print_success(f"{name}: PASS")
        else:
            print_error(f"{name}: FAIL")

    print(f"\n{BLUE}{'─' * 70}{RESET}")

    if passed == total:
        print_success(f"All checks passed! ({passed}/{total})")
        print(f"\n{GREEN}✓ Your environment is ready for deployment!{RESET}\n")
        return 0
    else:
        print_error(f"Some checks failed ({passed}/{total} passed)")
        print(f"\n{RED}✗ Please fix the issues above before deploying{RESET}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
