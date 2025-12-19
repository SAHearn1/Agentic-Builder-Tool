#!/bin/bash
# Script to help set up Vercel environment variables
# This script guides you through adding environment variables to Vercel

set -e

echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║       Vercel Environment Variables Setup Helper                   ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found"
    echo "   Run: cp .env.example .env"
    echo "   Then edit .env with your credentials"
    exit 1
fi

# Load .env
set -a
source .env 2>/dev/null
set +a

echo "📋 This script will guide you through setting up environment variables in Vercel."
echo "   You can do this via:"
echo "   1. Vercel Dashboard (https://vercel.com/dashboard)"
echo "   2. Vercel CLI (commands shown below)"
echo ""

# Check if vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "⚠️  Vercel CLI not found"
    echo "   Install it: npm install -g vercel"
    echo "   Then run this script again"
    echo ""
    echo "   Or use the Vercel Dashboard to add variables manually"
    SHOW_CLI=false
else
    echo "✓ Vercel CLI found"
    SHOW_CLI=true
fi

echo ""
echo "════════════════════════════════════════════════════════════════════"
echo "Required Environment Variables"
echo "════════════════════════════════════════════════════════════════════"
echo ""

# Function to show how to add a variable
show_variable() {
    local name=$1
    local value=$2
    local description=$3

    if [ -z "$value" ] || [ "$value" = "your_"* ]; then
        echo "❌ $name"
        echo "   Status: NOT SET in .env"
        echo "   Description: $description"
        echo "   → Set this in your .env file first!"
    else
        echo "✓ $name"
        echo "   Value: ${value:0:10}...${value: -4}"
        echo "   Description: $description"

        if [ "$SHOW_CLI" = true ]; then
            echo "   CLI Command:"
            echo "   vercel env add $name production"
            echo "   (paste value when prompted)"
        else
            echo "   Dashboard: Add in Project Settings → Environment Variables"
        fi
    fi
    echo ""
}

# Show all variables
show_variable "ANTHROPIC_API_KEY" "$ANTHROPIC_API_KEY" "Anthropic Claude API key"
show_variable "GITHUB_TOKEN" "$GITHUB_TOKEN" "GitHub personal access token"
show_variable "VERCEL_TOKEN" "$VERCEL_TOKEN" "Vercel API token"
show_variable "GCS_PROJECT_ID" "$GCS_PROJECT_ID" "Google Cloud project ID"
show_variable "GCS_BUCKET_NAME" "$GCS_BUCKET_NAME" "Google Cloud Storage bucket name"

echo "════════════════════════════════════════════════════════════════════"
echo "GCP Service Account Credentials (Special Handling)"
echo "════════════════════════════════════════════════════════════════════"
echo ""

if [ -f "$GOOGLE_APPLICATION_CREDENTIALS" ]; then
    echo "✓ Service account key file found: $GOOGLE_APPLICATION_CREDENTIALS"
    echo ""
    echo "⚠️  Vercel requires special handling for this file:"
    echo ""

    if [ "$SHOW_CLI" = true ]; then
        echo "Method 1: Using Vercel CLI (Recommended)"
        echo "  cat $GOOGLE_APPLICATION_CREDENTIALS | vercel secrets add gcp-credentials"
        echo "  vercel env add GOOGLE_APPLICATION_CREDENTIALS_JSON production"
        echo "  (then enter: @gcp-credentials)"
        echo ""
    fi

    echo "Method 2: Using Dashboard"
    echo "  1. Open $GOOGLE_APPLICATION_CREDENTIALS"
    echo "  2. Copy the entire JSON content"
    echo "  3. In Vercel Dashboard, add environment variable:"
    echo "     Name: GOOGLE_APPLICATION_CREDENTIALS_JSON"
    echo "     Value: <paste entire JSON>"
    echo ""
else
    echo "❌ Service account key file not found: $GOOGLE_APPLICATION_CREDENTIALS"
    echo "   Download your service account key from GCP Console"
    echo "   See SETUP_GUIDE.md for instructions"
fi

echo ""
echo "════════════════════════════════════════════════════════════════════"
echo "Application Configuration"
echo "════════════════════════════════════════════════════════════════════"
echo ""

echo "These variables configure your application settings:"
echo ""
echo "APP_ENV=production"
echo "APP_HOST=0.0.0.0"
echo "APP_PORT=8080"
echo "LOG_LEVEL=INFO"
echo "AGENT_MODEL=claude-3-5-sonnet-20241022"
echo "AGENT_TEMPERATURE=0.7"
echo "AGENT_MAX_ITERATIONS=10"
echo "ALLOWED_ORIGINS=https://your-app.vercel.app"
echo ""
echo "⚠️  Important: Replace 'your-app.vercel.app' with your actual Vercel domain!"
echo ""

if [ "$SHOW_CLI" = true ]; then
    echo "Quick add all application configs:"
    echo "  vercel env add APP_ENV production && echo 'production' | vercel env add APP_ENV production"
    echo "  vercel env add APP_PORT production && echo '8080' | vercel env add APP_PORT production"
    echo "  # ... (add each one)"
    echo ""
fi

echo "════════════════════════════════════════════════════════════════════"
echo "Next Steps"
echo "════════════════════════════════════════════════════════════════════"
echo ""

if [ "$SHOW_CLI" = true ]; then
    echo "Using Vercel CLI:"
    echo "  1. vercel login"
    echo "  2. vercel link"
    echo "  3. Add environment variables (see commands above)"
    echo "  4. vercel --prod"
    echo ""
fi

echo "Using Vercel Dashboard:"
echo "  1. Go to https://vercel.com/dashboard"
echo "  2. Select your project"
echo "  3. Go to Settings → Environment Variables"
echo "  4. Add each variable shown above"
echo "  5. Deploy your project"
echo ""

echo "📖 For detailed instructions, see:"
echo "   - VERCEL_DEPLOYMENT.md (complete Vercel guide)"
echo "   - SETUP_GUIDE.md (credential setup)"
echo ""

# Summary
MISSING=0
[ -z "$ANTHROPIC_API_KEY" ] || [ "$ANTHROPIC_API_KEY" = "your_"* ] && MISSING=$((MISSING + 1))
[ -z "$GITHUB_TOKEN" ] || [ "$GITHUB_TOKEN" = "your_"* ] && MISSING=$((MISSING + 1))
[ -z "$VERCEL_TOKEN" ] || [ "$VERCEL_TOKEN" = "your_"* ] && MISSING=$((MISSING + 1))
[ -z "$GCS_PROJECT_ID" ] || [ "$GCS_PROJECT_ID" = "your_"* ] && MISSING=$((MISSING + 1))
[ -z "$GCS_BUCKET_NAME" ] || [ "$GCS_BUCKET_NAME" = "your_"* ] && MISSING=$((MISSING + 1))

if [ $MISSING -eq 0 ]; then
    echo "✅ All required variables are set in your .env file"
    echo "   Now add them to Vercel using one of the methods above"
else
    echo "⚠️  $MISSING required variable(s) missing in .env"
    echo "   Edit your .env file first, then run this script again"
fi

echo ""
