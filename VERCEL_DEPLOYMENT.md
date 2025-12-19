# Deploying to Vercel

This guide covers deploying the Agentic Builder Tool to Vercel with proper environment variable configuration.

## Prerequisites

- Vercel account (free or paid)
- Vercel CLI installed (optional but recommended)
- All credentials ready (see SETUP_GUIDE.md)

---

## Method 1: Deploy via Vercel Dashboard (Recommended for First Time)

### Step 1: Import Your Repository

1. Go to https://vercel.com/dashboard
2. Click **"Add New..."** → **"Project"**
3. Import your GitHub repository: `SAHearn1/Agentic-Builder-Tool`
4. Select the repository and click **"Import"**

### Step 2: Configure Build Settings

Vercel should auto-detect the framework, but verify these settings:

**Framework Preset:** Other
**Build Command:** `pip install -e .`
**Output Directory:** (leave empty)
**Install Command:** `pip install -r requirements.txt` or `pip install -e .`

### Step 3: Add Environment Variables

Before deploying, click **"Environment Variables"** and add each of the following:

#### Required Variables:

| Variable Name | Value | Environment |
|--------------|-------|-------------|
| `ANTHROPIC_API_KEY` | Your Anthropic API key (sk-ant-api03-...) | Production, Preview, Development |
| `GITHUB_TOKEN` | Your GitHub personal access token (ghp_...) | Production, Preview, Development |
| `VERCEL_TOKEN` | Your Vercel API token | Production, Preview, Development |
| `GCS_PROJECT_ID` | Your Google Cloud project ID | Production, Preview, Development |
| `GCS_BUCKET_NAME` | Your GCS bucket name | Production, Preview, Development |
| `GOOGLE_APPLICATION_CREDENTIALS` | `/tmp/gcp-key.json` | Production, Preview, Development |

#### Application Configuration:

| Variable Name | Value | Environment |
|--------------|-------|-------------|
| `APP_ENV` | `production` | Production |
| `APP_HOST` | `0.0.0.0` | All |
| `APP_PORT` | `8080` | All |
| `LOG_LEVEL` | `INFO` | Production |
| `AGENT_MODEL` | `claude-3-5-sonnet-20241022` | All |
| `AGENT_TEMPERATURE` | `0.7` | All |
| `AGENT_MAX_ITERATIONS` | `10` | All |
| `ALLOWED_ORIGINS` | `https://your-domain.vercel.app` | Production |

**For each variable:**
1. Enter the **Name**
2. Enter the **Value**
3. Select which environments: Production, Preview, and/or Development
4. Click **"Add"**

### Step 4: Configure GCP Service Account (Special Handling)

Vercel doesn't support file uploads directly, so we need to handle the GCP service account key differently.

**Option A: Use Vercel CLI to add as secret (Recommended)**

```bash
# Install Vercel CLI if you haven't
npm install -g vercel

# Login
vercel login

# Link to your project
vercel link

# Add GCP credentials as a secret
# This reads your local file and uploads it securely
cat gcp-service-account-key.json | vercel secrets add gcp-credentials

# Then in dashboard, set environment variable:
# Name: GOOGLE_APPLICATION_CREDENTIALS_JSON
# Value: @gcp-credentials
```

**Option B: Add as environment variable (JSON string)**

1. Open your `gcp-service-account-key.json` file
2. Copy the **entire contents** (it's a JSON object)
3. In Vercel dashboard, add environment variable:
   - Name: `GOOGLE_APPLICATION_CREDENTIALS_JSON`
   - Value: Paste the entire JSON content
   - Important: This will be parsed at runtime

You'll need to update the code to handle this (see "Code Modifications" section below).

### Step 5: Deploy

Click **"Deploy"** button. Vercel will:
1. Clone your repository
2. Install dependencies
3. Set environment variables
4. Start your application

---

## Method 2: Deploy via Vercel CLI

### Step 1: Install and Login

```bash
# Install Vercel CLI
npm install -g vercel

# Login to your account
vercel login
```

### Step 2: Link Your Project

```bash
cd /home/user/Agentic-Builder-Tool

# Link to existing project or create new one
vercel link
```

### Step 3: Add Environment Variables via CLI

```bash
# Add each environment variable
vercel env add ANTHROPIC_API_KEY production
# Paste your API key when prompted

vercel env add GITHUB_TOKEN production
# Paste your GitHub token

vercel env add VERCEL_TOKEN production
# Paste your Vercel token

vercel env add GCS_PROJECT_ID production
# Enter your GCP project ID

vercel env add GCS_BUCKET_NAME production
# Enter your bucket name

# Add GCP credentials as secret
cat gcp-service-account-key.json | vercel secrets add gcp-credentials
vercel env add GOOGLE_APPLICATION_CREDENTIALS_JSON production
# Enter: @gcp-credentials

# Add application config
vercel env add APP_ENV production
# Enter: production

vercel env add APP_PORT production
# Enter: 8080

vercel env add ALLOWED_ORIGINS production
# Enter: https://your-domain.vercel.app
```

### Step 4: Deploy

```bash
# Deploy to production
vercel --prod

# Or deploy to preview
vercel
```

---

## Code Modifications for Vercel

Vercel's filesystem is read-only except for `/tmp`, so we need to handle the GCP credentials differently.

### Option 1: Modify src/tools/gcs_tools.py

Add this helper function at the top of the file:

```python
import json
import os
from google.cloud import storage
from google.oauth2 import service_account

def _get_storage_client():
    """Get Google Cloud Storage client with Vercel-compatible auth."""
    settings = get_settings()

    # Check if we have credentials as JSON string (Vercel deployment)
    creds_json = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON")

    if creds_json:
        # Parse JSON credentials from environment variable
        try:
            creds_dict = json.loads(creds_json)
            credentials = service_account.Credentials.from_service_account_info(creds_dict)
            return storage.Client(project=settings.gcs_project_id, credentials=credentials)
        except json.JSONDecodeError:
            # If it's a secret reference like @gcp-credentials, Vercel will inject actual JSON
            # Try again
            pass

    # Fall back to file-based credentials (local development)
    if settings.google_application_credentials:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.google_application_credentials

    return storage.Client(project=settings.gcs_project_id)
```

### Option 2: Create a Vercel-specific startup script

Create `vercel-build.sh`:

```bash
#!/bin/bash
# Vercel build script

# If GCP credentials are in environment variable, write to temp file
if [ ! -z "$GOOGLE_APPLICATION_CREDENTIALS_JSON" ]; then
    echo "$GOOGLE_APPLICATION_CREDENTIALS_JSON" > /tmp/gcp-key.json
    export GOOGLE_APPLICATION_CREDENTIALS=/tmp/gcp-key.json
fi

# Install dependencies
pip install -e .

echo "Build complete"
```

Update `vercel.json`:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "src/main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "src/main.py"
    }
  ],
  "env": {
    "PYTHONPATH": "/var/task"
  }
}
```

---

## Vercel Configuration File

Create `vercel.json` in your project root:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "src/main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "src/main.py"
    }
  ],
  "env": {
    "PYTHONPATH": "/var/task",
    "APP_PORT": "8080"
  },
  "regions": ["iad1"],
  "functions": {
    "src/main.py": {
      "memory": 1024,
      "maxDuration": 60
    }
  }
}
```

---

## Important Considerations for Vercel

### 1. **Serverless Functions**
Vercel runs Python apps as serverless functions with some limitations:
- **Max execution time**: 60 seconds (Hobby), 300 seconds (Pro)
- **Max payload size**: 4.5 MB
- **Read-only filesystem** except `/tmp`
- **Cold starts**: First request may be slow

### 2. **Port Configuration**
Vercel automatically handles port binding. Your app should:
- Listen on `0.0.0.0`
- Use port from `PORT` environment variable (Vercel sets this)
- Default to 8080 if PORT not set

Update `src/main.py`:

```python
if __name__ == "__main__":
    import uvicorn

    settings = get_settings()
    port = int(os.getenv("PORT", settings.app_port))

    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=port,
        reload=False,  # Disable reload in production
    )
```

### 3. **CORS Configuration**
Update `ALLOWED_ORIGINS` to your Vercel domain:

```bash
ALLOWED_ORIGINS=https://your-app.vercel.app,https://www.your-domain.com
```

### 4. **Logs and Monitoring**
- View logs in Vercel dashboard: Project → Deployments → [Select deployment] → Function Logs
- Real-time logs: `vercel logs`
- Monitor performance in Vercel Analytics

---

## Verify Deployment

After deployment completes:

### 1. Check Deployment URL
Vercel will provide a URL like: `https://agentic-builder-tool-xxx.vercel.app`

### 2. Test Health Endpoint
```bash
curl https://your-app.vercel.app/health
```

Expected response:
```json
{"status": "healthy", "version": "0.1.0"}
```

### 3. Test API Documentation
Visit: `https://your-app.vercel.app/docs`

### 4. Check Environment Variables
```bash
# List configured variables
vercel env ls
```

---

## Troubleshooting

### "Module not found" errors
**Fix:** Ensure `requirements.txt` or `pyproject.toml` includes all dependencies
```bash
pip freeze > requirements.txt
vercel --prod
```

### "Cannot connect to GCS"
**Fix:** Verify GOOGLE_APPLICATION_CREDENTIALS_JSON is set correctly
```bash
vercel env pull .env.production.local
cat .env.production.local | grep GOOGLE_APPLICATION_CREDENTIALS_JSON
```

### "Port already in use"
**Fix:** Use PORT environment variable
```python
port = int(os.getenv("PORT", 8080))
```

### "Function timeout"
**Fix:** Increase timeout in `vercel.json` (Pro plan required for >60s)
```json
"functions": {
  "src/main.py": {
    "maxDuration": 300
  }
}
```

### View Live Logs
```bash
vercel logs --follow
```

---

## Cost Considerations

**Vercel Hobby Plan (Free):**
- ✓ Unlimited deployments
- ✓ 100 GB bandwidth/month
- ✓ Serverless function execution
- ✗ 60 second max function timeout
- ✗ No custom domains on Hobby

**Vercel Pro ($20/month):**
- ✓ 1 TB bandwidth
- ✓ 300 second max timeout
- ✓ Custom domains
- ✓ Password protection
- ✓ Team collaboration

**Additional Costs:**
- Anthropic API usage (separate)
- Google Cloud Storage (separate)
- Vercel bandwidth overages if exceeded

---

## Alternative: Deploy to Cloud Run Instead

If Vercel's limitations are too restrictive, consider Google Cloud Run:
- Longer execution times (60 minutes)
- More memory (8 GB)
- Easier GCP integration
- Better for long-running agent operations

See `DEPLOYMENT.md` for Cloud Run instructions.

---

## Security Checklist

Before deploying to production:

- [ ] All environment variables configured in Vercel
- [ ] `ALLOWED_ORIGINS` set to your domain (not `*`)
- [ ] Secrets stored in Vercel (not in code)
- [ ] Service account has minimal required permissions
- [ ] API keys are not hardcoded anywhere
- [ ] `.env` file is gitignored
- [ ] Test deployment in Preview environment first
- [ ] Monitor logs for errors/unauthorized access

---

## Next Steps

1. **Configure environment variables** in Vercel dashboard
2. **Deploy** to preview environment first
3. **Test** all endpoints work correctly
4. **Monitor** logs and performance
5. **Deploy to production** when ready

For detailed credential setup, see `SETUP_GUIDE.md`
