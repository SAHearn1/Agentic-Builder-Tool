# Environment Setup Guide

This guide will help you configure all required credentials and verify your setup before deployment.

## Quick Start

1. **Copy the environment template**
   ```bash
   cp .env.example .env
   ```

2. **Edit .env with your credentials**
   ```bash
   nano .env  # or use your preferred editor
   ```

3. **Run the verification script**
   ```bash
   python verify_env.py
   ```

---

## Step-by-Step Setup

### Step 1: Anthropic API Key

1. Go to https://console.anthropic.com
2. Sign up or log in
3. Navigate to **API Keys**
4. Click **Create Key**
5. Copy the key (starts with `sk-ant-api03-`)

**Add to .env:**
```bash
ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
```

---

### Step 2: GitHub Personal Access Token

1. Go to GitHub → **Settings** → **Developer settings** → **Personal access tokens** → **Tokens (classic)**
2. Click **Generate new token (classic)**
3. Give it a name: `Agentic Builder Tool`
4. Set expiration: 90 days (recommended)
5. Select these scopes:
   - ✓ **repo** (Full control of private repositories)
   - ✓ **workflow** (Update GitHub Action workflows)
   - ✓ **admin:repo_hook** (Full control of repository hooks)
6. Click **Generate token**
7. Copy the token immediately (starts with `ghp_`)

**Add to .env:**
```bash
GITHUB_TOKEN=ghp_your-token-here
GITHUB_DEFAULT_ORG=your-github-username  # Optional
```

---

### Step 3: Vercel API Token

1. Go to https://vercel.com
2. Log in to your account
3. Go to **Settings** → **Tokens**
4. Click **Create Token**
5. Name: `Agentic Builder Tool`
6. Scope: Select your account or team
7. Expiration: 1 year (recommended)
8. Copy the token

**Add to .env:**
```bash
VERCEL_TOKEN=your-token-here
VERCEL_TEAM_ID=team_xxxxx  # Optional, only if using team account
```

**To get your Team ID (if needed):**
```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# List teams
vercel teams list
```

---

### Step 4: Google Cloud Platform Setup

#### 4.1 Create GCP Project

```bash
# Install Google Cloud SDK if you haven't
# Visit: https://cloud.google.com/sdk/docs/install

# Create project
PROJECT_ID="agentic-builder-prod"  # Choose your own
gcloud projects create $PROJECT_ID --name="Agentic Builder Tool"

# Set as default
gcloud config set project $PROJECT_ID

# Enable billing (required)
# Go to: https://console.cloud.google.com/billing
# Link your billing account to this project
```

#### 4.2 Enable Required APIs

```bash
gcloud services enable storage.googleapis.com
gcloud services enable cloudresourcemanager.googleapis.com
```

#### 4.3 Create Storage Bucket

```bash
# Choose a globally unique bucket name
BUCKET_NAME="agentic-builder-artifacts-$(date +%s)"
REGION="us-central1"  # Choose your region

# Create bucket
gcloud storage buckets create gs://$BUCKET_NAME \
  --location=$REGION \
  --uniform-bucket-level-access \
  --public-access-prevention

echo "Bucket created: $BUCKET_NAME"
```

#### 4.4 Create Service Account

```bash
SERVICE_ACCOUNT_NAME="agentic-builder-sa"
SERVICE_ACCOUNT_EMAIL="${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"

# Create service account
gcloud iam service-accounts create $SERVICE_ACCOUNT_NAME \
  --display-name="Agentic Builder Service Account"

# Grant Storage permissions
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:${SERVICE_ACCOUNT_EMAIL}" \
  --role="roles/storage.objectAdmin"

# Create and download key
gcloud iam service-accounts keys create gcp-service-account-key.json \
  --iam-account=$SERVICE_ACCOUNT_EMAIL

# Secure the file
chmod 600 gcp-service-account-key.json

echo "Service account key saved to: gcp-service-account-key.json"
```

**Add to .env:**
```bash
GCS_PROJECT_ID=agentic-builder-prod  # Your project ID
GCS_BUCKET_NAME=agentic-builder-artifacts-1234567890  # Your bucket name
GOOGLE_APPLICATION_CREDENTIALS=./gcp-service-account-key.json
```

---

### Step 5: Configure Application Settings

**Add to .env:**
```bash
# Application Configuration
APP_ENV=development
APP_HOST=0.0.0.0
APP_PORT=8000
LOG_LEVEL=INFO

# Agent Configuration
AGENT_MODEL=claude-3-5-sonnet-20241022
AGENT_TEMPERATURE=0.7
AGENT_MAX_ITERATIONS=10

# CORS Configuration (important for security!)
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

**For production, set specific domains:**
```bash
ALLOWED_ORIGINS=https://yourdomain.com,https://app.yourdomain.com
```

---

## Verification

After setting up all credentials, run the verification script:

```bash
python verify_env.py
```

This script will:
- ✓ Check if .env file exists
- ✓ Verify all environment variables are set
- ✓ Test connection to Anthropic API
- ✓ Test connection to GitHub API
- ✓ Test connection to Vercel API
- ✓ Test connection to Google Cloud Storage
- ✓ Verify GCP service account credentials
- ✓ Check dependencies are installed

**Expected output:**
```
✓ All checks passed! (9/9)
✓ Your environment is ready for deployment!
```

---

## Troubleshooting

### "ANTHROPIC_API_KEY not set"
- Make sure you've created `.env` file (not `.env.example`)
- Check there are no typos in the variable name
- Ensure there are no spaces around the `=` sign

### "Authentication failed" for any API
- Verify your token/key is correct
- Check if the token has expired
- Ensure the token has the required permissions/scopes

### "Bucket does not exist or is not accessible"
- Verify the bucket name is correct
- Check service account has `storage.objectAdmin` role
- Ensure the bucket is in the correct project

### "Service account key file not found"
- Check the path in `GOOGLE_APPLICATION_CREDENTIALS`
- Ensure the file is in the project root
- Verify the file name matches exactly

### "Dependencies not installed"
```bash
pip install -e ".[dev]"
```

---

## Security Checklist

Before committing any code:

- [ ] `.env` file is in `.gitignore`
- [ ] `gcp-service-account-key.json` is in `.gitignore` or covered by `*.json`
- [ ] Service account key has permissions `600` (read/write for owner only)
- [ ] No API keys are hardcoded in source files
- [ ] `ALLOWED_ORIGINS` is set to specific domains (not `*`) for production

**Check .gitignore:**
```bash
grep -E "^\.env$|^\*\.json$|^gcp-service-account-key\.json$" .gitignore
```

---

## Quick Commands Reference

**Test application locally:**
```bash
uvicorn src.main:app --reload
```

**Run with Docker Compose:**
```bash
docker-compose up -d
```

**Check logs:**
```bash
docker-compose logs -f
```

**Run tests:**
```bash
python -m pytest tests/ -v
```

**Stop application:**
```bash
docker-compose down
```

---

## GitHub Secrets (for CI/CD)

For automated deployments, add these secrets to your GitHub repository:

**Go to:** Repository → Settings → Secrets and variables → Actions → New repository secret

Add each of these:
```
Name: ANTHROPIC_API_KEY
Value: [your Anthropic API key]

Name: GITHUB_TOKEN
Value: [your GitHub token or use built-in GITHUB_TOKEN]

Name: VERCEL_TOKEN
Value: [your Vercel token]

Name: GCP_CREDENTIALS
Value: [entire contents of gcp-service-account-key.json file]

Name: GCS_PROJECT_ID
Value: [your GCP project ID]

Name: GCS_BUCKET_NAME
Value: [your GCS bucket name]
```

---

## Next Steps

Once verification passes:

1. **Test locally:**
   ```bash
   uvicorn src.main:app --reload
   ```
   Visit: http://localhost:8000/docs

2. **Run tests:**
   ```bash
   python -m pytest tests/ -v
   ```

3. **Try Docker:**
   ```bash
   docker-compose up
   ```

4. **Deploy to production** following the deployment guide in `DEPLOYMENT.md`

---

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Run `python verify_env.py` to diagnose the problem
3. Review the detailed setup guide in the main `README.md`
4. Check service-specific documentation:
   - [Anthropic API Docs](https://docs.anthropic.com/)
   - [GitHub API Docs](https://docs.github.com/en/rest)
   - [Vercel API Docs](https://vercel.com/docs/rest-api)
   - [Google Cloud Storage Docs](https://cloud.google.com/storage/docs)
