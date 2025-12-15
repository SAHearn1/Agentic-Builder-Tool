#!/usr/bin/env python3
"""Verification script to check the application structure and dependencies."""

import sys
from pathlib import Path


def check_file_exists(path: Path, description: str) -> bool:
    """Check if a file exists."""
    if path.exists():
        print(f"✓ {description}: {path}")
        return True
    else:
        print(f"✗ {description} missing: {path}")
        return False


def check_directory_exists(path: Path, description: str) -> bool:
    """Check if a directory exists."""
    if path.is_dir():
        print(f"✓ {description}: {path}")
        return True
    else:
        print(f"✗ {description} missing: {path}")
        return False


def main():
    """Main verification function."""
    print("=" * 70)
    print("Agentic Tool Builder - Structure Verification")
    print("=" * 70)
    print()

    root = Path(__file__).parent
    checks = []

    # Check core files
    print("Core Files:")
    checks.append(check_file_exists(root / "README.md", "README"))
    checks.append(check_file_exists(root / "pyproject.toml", "Project configuration"))
    checks.append(check_file_exists(root / "Dockerfile", "Dockerfile"))
    checks.append(check_file_exists(root / "docker-compose.yml", "Docker Compose"))
    checks.append(check_file_exists(root / ".env.example", "Environment example"))
    checks.append(check_file_exists(root / ".gitignore", "Gitignore"))
    checks.append(check_file_exists(root / "Makefile", "Makefile"))
    print()

    # Check source structure
    print("Source Structure:")
    checks.append(check_directory_exists(root / "src", "Source directory"))
    checks.append(check_directory_exists(root / "src" / "agent", "Agent module"))
    checks.append(check_directory_exists(root / "src" / "api", "API module"))
    checks.append(check_directory_exists(root / "src" / "config", "Config module"))
    checks.append(check_directory_exists(root / "src" / "models", "Models module"))
    checks.append(check_directory_exists(root / "src" / "tools", "Tools module"))
    print()

    # Check key source files
    print("Key Source Files:")
    checks.append(check_file_exists(root / "src" / "main.py", "Main application"))
    checks.append(
        check_file_exists(root / "src" / "agent" / "graph.py", "Agent graph")
    )
    checks.append(check_file_exists(root / "src" / "agent" / "state.py", "Agent state"))
    checks.append(
        check_file_exists(root / "src" / "config" / "settings.py", "Settings")
    )
    checks.append(check_file_exists(root / "src" / "api" / "routes.py", "API routes"))
    print()

    # Check tools
    print("DevOps Tools:")
    checks.append(
        check_file_exists(root / "src" / "tools" / "github_tools.py", "GitHub tools")
    )
    checks.append(
        check_file_exists(root / "src" / "tools" / "vercel_tools.py", "Vercel tools")
    )
    checks.append(
        check_file_exists(root / "src" / "tools" / "gcs_tools.py", "GCS tools")
    )
    print()

    # Check test structure
    print("Test Structure:")
    checks.append(check_directory_exists(root / "tests", "Tests directory"))
    checks.append(check_directory_exists(root / "tests" / "unit", "Unit tests"))
    checks.append(
        check_directory_exists(root / "tests" / "integration", "Integration tests")
    )
    print()

    # Check documentation
    print("Documentation:")
    checks.append(check_file_exists(root / "USAGE.md", "Usage guide"))
    checks.append(check_file_exists(root / "DEPLOYMENT.md", "Deployment guide"))
    print()

    # Try to import the package
    print("Package Import Test:")
    try:
        sys.path.insert(0, str(root))
        import src

        print(f"✓ Package can be imported (version: {src.__version__})")
        checks.append(True)
    except ImportError as e:
        print(f"✗ Package import failed: {e}")
        checks.append(False)
    print()

    # Summary
    print("=" * 70)
    passed = sum(checks)
    total = len(checks)
    percentage = (passed / total) * 100 if total > 0 else 0

    print(f"Verification Summary: {passed}/{total} checks passed ({percentage:.1f}%)")
    print("=" * 70)

    if passed == total:
        print("✓ All checks passed! The application structure is complete.")
        return 0
    else:
        print("✗ Some checks failed. Please review the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
