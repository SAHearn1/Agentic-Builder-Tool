# GitHub Actions Workflows

## Deploy to Cloud Run

This workflow automatically deploys the application to Google Cloud Run when changes are pushed to the `main` branch.

### Prerequisites

Before the workflow can run successfully, you need to complete the following setup steps:

#### 1. Update Workflow Environment Variables

Edit `.github/workflows/deploy.yaml` and update the following environment variables:

```yaml
env:
  PROJECT_ID: your-google-project-id  # <--- UPDATE THIS
  REGION: us-central1                 # <--- UPDATE THIS (or keep default)
  REPO_NAME: my-devops-agent          # Name of your Artifact Registry Repo
  SERVICE_NAME: devops-agent          # Name of your Cloud Run Service
```

#### 2. Create Google Cloud Service Account

Run these commands in your terminal to create a service account with the necessary permissions:

```bash
# 1. Create a Service Account for GitHub
gcloud iam service-accounts create github-deployer \
  --display-name="GitHub Actions Deployer"

# 2. Give it permission to Push to Registry & Deploy to Run
gcloud projects add-iam-policy-binding [YOUR_PROJECT_ID] \
  --member="serviceAccount:github-deployer@[YOUR_PROJECT_ID].iam.gserviceaccount.com" \
  --role="roles/run.admin"

gcloud projects add-iam-policy-binding [YOUR_PROJECT_ID] \
  --member="serviceAccount:github-deployer@[YOUR_PROJECT_ID].iam.gserviceaccount.com" \
  --role="roles/storage.admin"

gcloud projects add-iam-policy-binding [YOUR_PROJECT_ID] \
  --member="serviceAccount:github-deployer@[YOUR_PROJECT_ID].iam.gserviceaccount.com" \
  --role="roles/artifactregistry.writer"

gcloud projects add-iam-policy-binding [YOUR_PROJECT_ID] \
  --member="serviceAccount:github-deployer@[YOUR_PROJECT_ID].iam.gserviceaccount.com" \
  --role="roles/iam.serviceAccountUser"

# 3. Download the Key File
gcloud iam service-accounts keys create key.json \
  --iam-account=github-deployer@[YOUR_PROJECT_ID].iam.gserviceaccount.com
```

**Important:** Replace `[YOUR_PROJECT_ID]` with your actual Google Cloud project ID in all commands above.

#### 3. Create Artifact Registry Repository

Create the Docker repository in Google Artifact Registry:

```bash
gcloud artifacts repositories create my-devops-agent \
  --repository-format=docker \
  --location=us-central1 \
  --description="Docker repository for DevOps Agent"
```

**Note:** If you changed `REPO_NAME` in the workflow, use that name instead of `my-devops-agent`.

#### 4. Add GitHub Secrets

Go to your GitHub repository: **Settings → Secrets and variables → Actions**

Click **New repository secret** and add the following secrets:

| Secret Name | Description |
|------------|-------------|
| `GCP_CREDENTIALS` | Paste the entire content of the `key.json` file you created in step 2 |
| `ANTHROPIC_API_KEY` | Your Anthropic API key for Claude |
| `GITHUB_ACCESS_TOKEN` | Your GitHub Personal Access Token |
| `VERCEL_TOKEN` | Your Vercel API token |

**Security Note:** After adding the `GCP_CREDENTIALS` secret to GitHub, delete the local `key.json` file to prevent accidental exposure.

### How It Works

The workflow performs the following steps:

1. **Checkout code** - Gets the latest code from the repository
2. **Google Auth** - Authenticates with Google Cloud using the service account
3. **Setup Cloud SDK** - Installs and configures the gcloud CLI
4. **Docker Auth** - Configures Docker to push to Google Artifact Registry
5. **Build and Push Container** - Builds the Docker image and pushes it to Artifact Registry
6. **Deploy to Cloud Run** - Deploys the container to Cloud Run with the specified environment variables

### Deployment Configuration

The application will be deployed with the following environment variables automatically set:

- `ANTHROPIC_API_KEY` - From GitHub secrets
- `GITHUB_ACCESS_TOKEN` - From GitHub secrets
- `VERCEL_TOKEN` - From GitHub secrets
- `GOOGLE_APPLICATION_CREDENTIALS` - Set to `google-credentials.json`

### Triggering the Workflow

The workflow is triggered automatically when you push commits to the `main` branch:

```bash
git push origin main
```

You can monitor the deployment progress in the **Actions** tab of your GitHub repository.

### Troubleshooting

If the workflow fails, check the following:

1. **Service Account Permissions** - Ensure all IAM roles are correctly assigned
2. **Artifact Registry** - Verify the repository exists in the correct region
3. **GitHub Secrets** - Confirm all required secrets are set with correct values
4. **Environment Variables** - Double-check that PROJECT_ID, REGION, etc. are updated in the workflow file
5. **Dockerfile** - Ensure the Dockerfile builds successfully locally

### Additional Resources

- [Google Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Google Artifact Registry Documentation](https://cloud.google.com/artifact-registry/docs)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [google-github-actions/auth](https://github.com/google-github-actions/auth)
- [google-github-actions/deploy-cloudrun](https://github.com/google-github-actions/deploy-cloudrun)
