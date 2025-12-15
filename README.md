# DevOps-Builder: Autonomous DevOps Agent

An intelligent, production-ready DevOps agent powered by **Claude 3.5 Sonnet** and **LangGraph**. This agent acts as an autonomous DevOps engineer capable of managing code deployments, infrastructure, and automation tasks using GitHub, Vercel, and Google Cloud Storage.

## 🚀 Features

- **AI-Powered DevOps**: Uses Claude 3.5 Sonnet via LangGraph for intelligent decision-making
- **GitHub Integration**: Full repository management capabilities via LangChain's GitHub toolkit
- **Vercel Deployments**: Trigger and manage Vercel deployments programmatically
- **Cloud Logging**: Build status logging to Google Cloud Storage
- **Production-Ready**: FastAPI server with LangServe, Docker support, and Cloud Run optimization

## 📋 Prerequisites

- Python 3.11 or higher
- Docker (for containerized deployment)
- API Keys:
  - Anthropic API key (for Claude)
  - GitHub Personal Access Token
  - Vercel Token
  - Google Cloud Service Account JSON (for GCS)

## ⚙️ Setup

### 1. Clone the Repository

```bash
git clone https://github.com/SAHearn1/Agentic-Builder-Tool.git
cd Agentic-Builder-Tool
```

### 2. Configure Environment Variables

Copy the example environment file and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```env
ANTHROPIC_API_KEY=your_anthropic_api_key_here
GITHUB_ACCESS_TOKEN=your_github_personal_access_token_here
VERCEL_TOKEN=your_vercel_token_here
GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/service-account-key.json
GCS_BUCKET_NAME=your_gcs_bucket_name_here
PORT=8080
```

### 3. Local Development Setup

#### Option A: Using Python Virtual Environment

```bash
# Create and activate virtual environment
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python server.py
```

#### Option B: Using Docker

```bash
# Build the Docker image
docker build -t devops-builder .

# Run the container
docker run -p 8080:8080 --env-file .env devops-builder
```

## 🐳 Docker Deployment

### Build the Image

```bash
docker build -t devops-builder:latest .
```

### Run Locally

```bash
docker run -p 8080:8080 \
  -e ANTHROPIC_API_KEY=your_key \
  -e GITHUB_ACCESS_TOKEN=your_token \
  -e VERCEL_TOKEN=your_token \
  -e GOOGLE_APPLICATION_CREDENTIALS=/app/service-account.json \
  -e GCS_BUCKET_NAME=your_bucket \
  -v /path/to/service-account.json:/app/service-account.json \
  devops-builder:latest
```

### Deploy to Google Cloud Run

```bash
# Tag the image for Google Container Registry
docker tag devops-builder:latest gcr.io/YOUR_PROJECT_ID/devops-builder:latest

# Push to GCR
docker push gcr.io/YOUR_PROJECT_ID/devops-builder:latest

# Deploy to Cloud Run
gcloud run deploy devops-builder \
  --image gcr.io/YOUR_PROJECT_ID/devops-builder:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars ANTHROPIC_API_KEY=your_key,GITHUB_ACCESS_TOKEN=your_token,VERCEL_TOKEN=your_token,GCS_BUCKET_NAME=your_bucket
```

## 📡 API Endpoints

Once running, the server exposes the following endpoints:

- **`GET /`** - Health check and service info
- **`GET /health`** - Health status
- **`POST /agent/invoke`** - Invoke the agent with a single request
- **`POST /agent/batch`** - Batch process multiple requests
- **`POST /agent/stream`** - Stream agent responses
- **`GET /agent/playground`** - Interactive web UI for testing
- **`GET /docs`** - OpenAPI/Swagger documentation

### Example Usage

```bash
# Test the health endpoint
curl http://localhost:8080/health

# Invoke the agent
curl -X POST http://localhost:8080/agent/invoke \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "messages": [
        {
          "role": "user",
          "content": "Deploy my-app to Vercel production"
        }
      ]
    },
    "config": {
      "configurable": {
        "thread_id": "example-thread"
      }
    }
  }'
```

## 🛠️ Available Tools

The agent has access to the following tools:

1. **GitHub Toolkit**: Repository management, issues, PRs, commits, etc.
2. **Vercel Deployment**: Trigger deployments to Vercel
3. **GCS Build Logging**: Log build statuses to Google Cloud Storage

## 🧪 Testing

```bash
# Run with verbose logging
python server.py

# Access the playground UI
open http://localhost:8080/agent/playground
```

## 📚 Tech Stack

- **Language**: Python 3.11+
- **Agent Framework**: LangGraph (ReAct agent pattern)
- **LLM**: Claude 3.5 Sonnet (Anthropic)
- **API Framework**: FastAPI + LangServe
- **Deployment**: Docker + Google Cloud Run
- **Integrations**: GitHub, Vercel, Google Cloud Storage

## 🔐 Security Notes

- Never commit `.env` files or credentials to version control
- Use service accounts with minimal required permissions for GCS
- Rotate API tokens regularly
- Consider using secret management services (e.g., Google Secret Manager) for production

## 📝 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request.
