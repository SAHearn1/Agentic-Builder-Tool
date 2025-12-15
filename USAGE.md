# Usage Guide

This guide demonstrates how to use the Agentic Tool Builder for various DevOps tasks.

## Table of Contents

1. [Quick Start](#quick-start)
2. [API Usage](#api-usage)
3. [Example Tasks](#example-tasks)
4. [LangServe Integration](#langserve-integration)

## Quick Start

### Starting the Application

```bash
# Using Python
uvicorn src.main:app --reload

# Using Docker
docker-compose up
```

The API will be available at `http://localhost:8000`.

### Your First Task

```bash
curl -X POST "http://localhost:8000/agent/task" \
  -H "Content-Type: application/json" \
  -d '{
    "task": "List all my GitHub repositories",
    "context": "Show only public repositories"
  }'
```

## API Usage

### Health Check

Check if the service is running:

```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "version": "0.1.0"
}
```

### Agent Status

Get agent configuration and status:

```bash
curl http://localhost:8000/agent/status
```

Response:
```json
{
  "status": "ready",
  "version": "0.1.0",
  "description": "Autonomous DevOps Agent"
}
```

### Execute Agent Task

Submit a task to the autonomous agent:

```bash
curl -X POST "http://localhost:8000/agent/task" \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Create a new repository called test-app",
    "context": "Make it private with a README",
    "max_iterations": 5
  }'
```

Response:
```json
{
  "success": true,
  "message": "Successfully created repository: https://github.com/user/test-app",
  "artifacts": ["https://github.com/user/test-app"],
  "metadata": {
    "iterations": 2,
    "deployment_status": "completed"
  }
}
```

## Example Tasks

### 1. GitHub Operations

#### Create a Repository

```bash
curl -X POST "http://localhost:8000/agent/task" \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Create a new GitHub repository named my-awesome-project",
    "context": "It should be public with a description: A sample project"
  }'
```

#### Commit Code to Repository

```bash
curl -X POST "http://localhost:8000/agent/task" \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Create a simple Python hello world script and commit it to username/my-repo",
    "context": "Commit to main branch with message: Initial commit"
  }'
```

#### Create Pull Request

```bash
curl -X POST "http://localhost:8000/agent/task" \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Create a pull request in username/my-repo from dev to main",
    "context": "Title: Add new feature, Body: This PR adds feature X"
  }'
```

### 2. Vercel Deployments

#### Create and Deploy Project

```bash
curl -X POST "http://localhost:8000/agent/task" \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Create a Vercel project and deploy the repository username/my-app",
    "context": "Use Next.js framework"
  }'
```

#### Check Deployment Status

```bash
curl -X POST "http://localhost:8000/agent/task" \
  -H "Content-Type: application/json" \
  -d '{
    "task": "List recent deployments for my-vercel-project",
    "context": "Show last 5 deployments"
  }'
```

### 3. Google Cloud Storage

#### Upload Artifact

```bash
curl -X POST "http://localhost:8000/agent/task" \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Upload a configuration file to Google Cloud Storage",
    "context": "File content: {\"env\": \"prod\"}, Path: configs/app.json"
  }'
```

#### List Storage Files

```bash
curl -X POST "http://localhost:8000/agent/task" \
  -H "Content-Type: application/json" \
  -d '{
    "task": "List all files in my GCS bucket",
    "context": "Show files in the configs/ folder"
  }'
```

### 4. Complex Workflows

#### Full CI/CD Pipeline

```bash
curl -X POST "http://localhost:8000/agent/task" \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Create a complete CI/CD workflow",
    "context": "1. Create a GitHub repo, 2. Add a Next.js app, 3. Deploy to Vercel, 4. Store build artifacts in GCS",
    "max_iterations": 15
  }'
```

## LangServe Integration

The application provides LangServe endpoints for direct agent interaction:

### Synchronous Invocation

```bash
curl -X POST "http://localhost:8000/agent/invoke" \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "messages": [
        {"role": "user", "content": "List my GitHub repositories"}
      ],
      "task": "List repositories",
      "code_generated": "",
      "deployment_status": "pending",
      "artifacts": [],
      "iteration_count": 0
    }
  }'
```

### Streaming Responses

```bash
curl -X POST "http://localhost:8000/agent/stream" \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "messages": [
        {"role": "user", "content": "Create a new repository"}
      ],
      "task": "Create repository",
      "code_generated": "",
      "deployment_status": "pending",
      "artifacts": [],
      "iteration_count": 0
    }
  }'
```

## Python Client Example

```python
import requests

class AgenticToolBuilderClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
    
    def execute_task(self, task, context=None, max_iterations=None):
        """Execute a DevOps task."""
        payload = {"task": task}
        if context:
            payload["context"] = context
        if max_iterations:
            payload["max_iterations"] = max_iterations
        
        response = requests.post(
            f"{self.base_url}/agent/task",
            json=payload
        )
        return response.json()
    
    def check_health(self):
        """Check service health."""
        response = requests.get(f"{self.base_url}/health")
        return response.json()

# Usage
client = AgenticToolBuilderClient()

# Check health
health = client.check_health()
print(f"Status: {health['status']}")

# Execute task
result = client.execute_task(
    task="Create a new GitHub repository called test-repo",
    context="Make it public"
)
print(f"Success: {result['success']}")
print(f"Message: {result['message']}")
```

## JavaScript/TypeScript Client Example

```typescript
interface TaskRequest {
  task: string;
  context?: string;
  max_iterations?: number;
}

interface AgentResponse {
  success: boolean;
  message: string;
  artifacts?: string[];
  metadata?: Record<string, any>;
}

class AgenticToolBuilderClient {
  constructor(private baseUrl: string = 'http://localhost:8000') {}

  async executeTask(request: TaskRequest): Promise<AgentResponse> {
    const response = await fetch(`${this.baseUrl}/agent/task`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
  }

  async checkHealth() {
    const response = await fetch(`${this.baseUrl}/health`);
    return await response.json();
  }
}

// Usage
const client = new AgenticToolBuilderClient();

const result = await client.executeTask({
  task: 'Deploy my app to Vercel',
  context: 'Use the main branch',
  max_iterations: 10,
});

console.log('Success:', result.success);
console.log('Message:', result.message);
```

## Best Practices

1. **Be Specific**: Provide clear, detailed task descriptions
2. **Add Context**: Include relevant context to help the agent make better decisions
3. **Set Limits**: Use `max_iterations` to prevent runaway executions
4. **Handle Errors**: Always check the `success` field in responses
5. **Monitor**: Check logs and artifacts for debugging
6. **Iterate**: Start with simple tasks and build up to complex workflows

## Troubleshooting

### Task Fails with Timeout

Increase `max_iterations`:
```json
{
  "task": "your task",
  "max_iterations": 20
}
```

### Authentication Errors

Verify your API keys in `.env`:
- Check `ANTHROPIC_API_KEY`
- Check `GITHUB_TOKEN`
- Check `VERCEL_TOKEN`
- Check GCS credentials

### Tool Not Working

Check tool-specific configuration:
- GitHub: Ensure token has required permissions
- Vercel: Verify team ID if using team account
- GCS: Check service account permissions

## Interactive Documentation

Visit the interactive API documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These provide:
- Interactive request testing
- Complete API schema
- Example requests and responses
- Authentication requirements
