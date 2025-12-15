# Deployment Guide

This guide covers deploying the Agentic Tool Builder to various platforms.

## Table of Contents

1. [Docker Deployment](#docker-deployment)
2. [Cloud Deployment](#cloud-deployment)
3. [Environment Configuration](#environment-configuration)
4. [Security Best Practices](#security-best-practices)

## Docker Deployment

### Using Docker Compose (Recommended)

1. **Prepare environment variables**:
```bash
cp .env.example .env
# Edit .env with your production credentials
```

2. **Build and start services**:
```bash
docker-compose up -d
```

3. **Check logs**:
```bash
docker-compose logs -f agentic-tool-builder
```

4. **Stop services**:
```bash
docker-compose down
```

### Using Docker Directly

1. **Build the image**:
```bash
docker build -t agentic-tool-builder:latest .
```

2. **Run the container**:
```bash
docker run -d \
  --name agentic-tool-builder \
  -p 8000:8000 \
  --env-file .env \
  agentic-tool-builder:latest
```

## Cloud Deployment

### Google Cloud Run

1. **Build and push to Container Registry**:
```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/agentic-tool-builder
```

2. **Deploy to Cloud Run**:
```bash
gcloud run deploy agentic-tool-builder \
  --image gcr.io/PROJECT_ID/agentic-tool-builder \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY,GITHUB_TOKEN=$GITHUB_TOKEN
```

### AWS ECS

1. **Create ECR repository**:
```bash
aws ecr create-repository --repository-name agentic-tool-builder
```

2. **Build and push image**:
```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com
docker build -t agentic-tool-builder .
docker tag agentic-tool-builder:latest ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/agentic-tool-builder:latest
docker push ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/agentic-tool-builder:latest
```

3. **Create ECS Task Definition and Service** (use AWS Console or CLI)

### Azure Container Instances

1. **Create a resource group**:
```bash
az group create --name agentic-tool-builder-rg --location eastus
```

2. **Deploy container**:
```bash
az container create \
  --resource-group agentic-tool-builder-rg \
  --name agentic-tool-builder \
  --image agentic-tool-builder:latest \
  --dns-name-label agentic-tool-builder \
  --ports 8000 \
  --environment-variables \
    ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY \
    GITHUB_TOKEN=$GITHUB_TOKEN \
    VERCEL_TOKEN=$VERCEL_TOKEN
```

## Environment Configuration

### Production Environment Variables

Create a `.env.production` file with production values:

```bash
# API Keys (DO NOT commit to version control)
ANTHROPIC_API_KEY=your_production_anthropic_key
GITHUB_TOKEN=your_production_github_token
VERCEL_TOKEN=your_production_vercel_token
GCS_PROJECT_ID=your_production_gcp_project
GCS_BUCKET_NAME=your_production_bucket
GOOGLE_APPLICATION_CREDENTIALS=/app/gcp-key.json

# Application Settings
APP_ENV=production
APP_HOST=0.0.0.0
APP_PORT=8000
LOG_LEVEL=INFO

# Agent Configuration
AGENT_MODEL=claude-3-5-sonnet-20241022
AGENT_TEMPERATURE=0.7
AGENT_MAX_ITERATIONS=10
```

### Secrets Management

For production deployments, use proper secrets management:

- **Docker Secrets**: Use Docker secrets for sensitive data
- **Cloud KMS**: Use cloud provider key management services
- **HashiCorp Vault**: Use Vault for centralized secrets management
- **Environment Variables**: Set via cloud platform's secret management

Example with Docker Secrets:
```bash
echo "your_api_key" | docker secret create anthropic_api_key -
```

## Security Best Practices

### 1. API Keys and Secrets

- Never commit API keys to version control
- Use environment variables or secrets management
- Rotate keys regularly
- Use least privilege principle for service accounts

### 2. Network Security

- Use HTTPS in production
- Configure firewall rules to restrict access
- Use VPC/private networks when possible
- Enable authentication on API endpoints

### 3. Container Security

- Use minimal base images
- Run containers as non-root user
- Scan images for vulnerabilities
- Keep dependencies updated

### 4. Monitoring and Logging

- Enable application logging
- Set up health checks
- Monitor resource usage
- Set up alerts for errors

### 5. Backup and Recovery

- Backup environment configuration
- Document deployment procedures
- Test disaster recovery procedures
- Keep rollback procedures ready

## Health Checks

The application provides a health check endpoint at `/health`:

```bash
curl http://localhost:8000/health
```

Configure your orchestrator to use this for liveness/readiness probes:

```yaml
# Kubernetes example
livenessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 10
  periodSeconds: 30

readinessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 5
  periodSeconds: 10
```

## Scaling

### Horizontal Scaling

The application is stateless and can be horizontally scaled:

```bash
docker-compose up -d --scale agentic-tool-builder=3
```

### Load Balancing

Use a load balancer (nginx, traefik, cloud load balancer) to distribute traffic:

```nginx
upstream agentic_backend {
    server localhost:8001;
    server localhost:8002;
    server localhost:8003;
}

server {
    listen 80;
    location / {
        proxy_pass http://agentic_backend;
    }
}
```

## Troubleshooting

### Check logs
```bash
docker logs agentic-tool-builder
```

### Access container shell
```bash
docker exec -it agentic-tool-builder /bin/bash
```

### Test connectivity
```bash
curl http://localhost:8000/
curl http://localhost:8000/health
```

### Common Issues

1. **Port already in use**: Change `APP_PORT` in `.env`
2. **API key errors**: Verify all required environment variables are set
3. **Import errors**: Ensure all dependencies are installed
4. **Permission errors**: Check file permissions and user context
