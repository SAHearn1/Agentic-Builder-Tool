#!/bin/bash
# Quick environment check script
# For detailed verification, run: python verify_env.py

echo "🔍 Quick Environment Check"
echo "=========================="
echo ""

# Check .env file
if [ -f .env ]; then
    echo "✓ .env file exists"
else
    echo "✗ .env file not found"
    echo "  Run: cp .env.example .env"
    exit 1
fi

# Load .env
set -a
source .env 2>/dev/null
set +a

# Check required variables
MISSING=0

check_var() {
    if [ -z "${!1}" ]; then
        echo "✗ $1 not set"
        MISSING=$((MISSING + 1))
    else
        echo "✓ $1 is set"
    fi
}

echo ""
echo "Required Variables:"
check_var "ANTHROPIC_API_KEY"
check_var "GITHUB_TOKEN"
check_var "VERCEL_TOKEN"
check_var "GCS_PROJECT_ID"
check_var "GCS_BUCKET_NAME"

echo ""
echo "Optional Variables:"
if [ -n "$GOOGLE_APPLICATION_CREDENTIALS" ]; then
    echo "✓ GOOGLE_APPLICATION_CREDENTIALS: $GOOGLE_APPLICATION_CREDENTIALS"
    if [ ! -f "$GOOGLE_APPLICATION_CREDENTIALS" ]; then
        echo "  ⚠ Warning: File not found at $GOOGLE_APPLICATION_CREDENTIALS"
    fi
else
    echo "⚠ GOOGLE_APPLICATION_CREDENTIALS not set"
fi

echo ""
echo "=========================="
if [ $MISSING -eq 0 ]; then
    echo "✓ Basic environment check passed"
    echo ""
    echo "For detailed verification including API connectivity tests:"
    echo "  python verify_env.py"
    exit 0
else
    echo "✗ $MISSING required variable(s) missing"
    echo ""
    echo "Edit your .env file and set the missing variables"
    echo "See SETUP_GUIDE.md for detailed instructions"
    exit 1
fi
