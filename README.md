# Agentic Tool Builder

> **Autonomous DevOps Agent using LangGraph, FastAPI, and Cloud Tools**

An intelligent, production-ready Python application that acts as an autonomous DevOps engineer. It leverages Anthropic's Claude 3.5 Sonnet via LangGraph to write code, manage GitHub repositories, deploy to Vercel, and store artifacts in Google Cloud Storage.

## 🚀 Features

- **Autonomous Agent**: LangGraph-powered agent with Claude 3.5 Sonnet for intelligent decision-making
- **GitHub Integration**: Create repositories, commit code, manage pull requests
- **Vercel Deployment**: Automated deployment and project management
- **Cloud Storage**: Artifact management with Google Cloud Storage
- **Production-Ready API**: FastAPI with LangServe for robust API endpoints
- **Docker Support**: Containerized deployment with Docker and Docker Compose
- **Type Safety**: Full Pydantic models with type hints
- **Extensible**: Easy to add new tools and capabilities

## 📋 Prerequisites

- Python 3.11 or higher
- Docker (optional, for containerized deployment)
- API Keys:
  - Anthropic API key
  - GitHub Personal Access Token
  - Vercel API Token
  - Google Cloud Platform Service Account

## 🛠️ Installation

### Local Development

1. **Clone the repository**:
```bash
git clone https://github.com/SAHearn1/Agentic-Builder-Tool.git
cd Agentic-Builder-Tool
```

2. **Create a virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -e ".[dev]"
```

4. **Configure environment variables**:
```bash
cp .env.example .env
# Edit .env with your actual API keys and configuration
```

5. **Verify your configuration**:
```bash
# Quick check (fast)
./quick_check.sh

# Comprehensive verification with API tests (recommended)
python verify_env.py
```

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed setup instructions.

6. **Run the application**:
```bash
uvicorn src.main:app --reload
```

The API will be available at `http://localhost:8000`.

### Docker Deployment

1. **Build and run with Docker Compose**:
```bash
docker-compose up -d
```

2. **View logs**:
```bash
docker-compose logs -f
```

3. **Stop the application**:
```bash
docker-compose down
```

## 🔧 Configuration

All configuration is done through environment variables. See `.env.example` for all available options:

| Variable | Description | Required |
|----------|-------------|----------|
| `ANTHROPIC_API_KEY` | Anthropic API key for Claude | Yes |
| `GITHUB_TOKEN` | GitHub personal access token | Yes |
| `VERCEL_TOKEN` | Vercel API token | Yes |
| `GCS_PROJECT_ID` | Google Cloud project ID | Yes |
| `GCS_BUCKET_NAME` | GCS bucket name | Yes |
| `GOOGLE_APPLICATION_CREDENTIALS` | Path to GCP service account key | Yes |
| `AGENT_MODEL` | Claude model to use | No (default: claude-3-5-sonnet-20241022) |
| `AGENT_MAX_ITERATIONS` | Maximum agent iterations | No (default: 10) |

### Environment Verification

Before running the application, verify your configuration:

**Quick Check** (basic validation):
```bash
./quick_check.sh
```

**Comprehensive Verification** (includes API connectivity tests):
```bash
python verify_env.py
```

The verification script will:
- ✓ Check all required environment variables
- ✓ Test connectivity to Anthropic, GitHub, Vercel, and GCS APIs
- ✓ Validate GCP service account credentials
- ✓ Verify bucket access and permissions
- ✓ Provide detailed error messages for any issues

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed credential setup instructions.

## 📚 API Documentation

Once the application is running, visit:
- **Interactive API Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

### Key Endpoints

#### Health Check
```bash
GET /health
```

#### Execute Agent Task
```bash
POST /agent/task
Content-Type: application/json

{
  "task": "Create a new React app and deploy it to Vercel",
  "context": "Use TypeScript and Tailwind CSS",
  "max_iterations": 10
}
```

#### LangServe Endpoints
```bash
POST /agent/invoke    # Synchronous agent invocation
POST /agent/stream    # Streaming agent responses
```

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/unit/test_config.py
```

## 🏗️ Architecture

```
src/
├── agent/          # LangGraph agent implementation
│   ├── graph.py    # Agent graph definition
│   └── state.py    # Agent state management
├── api/            # FastAPI routes
│   └── routes.py   # API endpoints
├── config/         # Configuration management
│   └── settings.py # Pydantic settings
├── models/         # Data models
│   ├── requests.py # Request models
│   └── responses.py# Response models
├── tools/          # DevOps tools
│   ├── github_tools.py  # GitHub integration
│   ├── vercel_tools.py  # Vercel deployment
│   └── gcs_tools.py     # Google Cloud Storage
└── main.py         # FastAPI application
```

## 🔨 Development

### Code Quality

Format code with Black:
```bash
black src/ tests/
```

Lint code with Ruff:
```bash
ruff check src/ tests/
```

Type checking with mypy:
```bash
mypy src/
```

### Adding New Tools

1. Create a new file in `src/tools/`
2. Define tools using the `@tool` decorator
3. Export the tools list
4. Update `src/tools/__init__.py` to include new tools

Example:
```python
from langchain_core.tools import tool

@tool
def my_new_tool(param: str) -> str:
    """Tool description."""
    # Implementation
    return "result"

my_tools = [my_new_tool]
```

## 🐳 Docker

### Build Image
```bash
docker build -t agentic-tool-builder .
```

### Run Container
```bash
docker run -p 8000:8000 --env-file .env agentic-tool-builder
```

## 📄 License

MIT License - see LICENSE file for details

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

For issues and questions, please open an issue on GitHub.

## 🙏 Acknowledgments

- Built with [LangGraph](https://github.com/langchain-ai/langgraph)
- Powered by [Anthropic Claude](https://www.anthropic.com/claude)
- API framework by [FastAPI](https://fastapi.tiangolo.com/)
- Served with [LangServe](https://github.com/langchain-ai/langserve)
