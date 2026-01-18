# DataMAx - Deployment Guide

## Docker Deployment

### Prerequisites
- Docker 20.10+
- Docker Compose 2.0+

### Quick Start with Docker

```bash
# Make setup script executable
chmod +x scripts/setup.sh

# Run setup script
./scripts/setup.sh
```

This will:
1. Build all Docker images
2. Start PostgreSQL, Backend, and Frontend services
3. Initialize the database with schema and seed data
4. Run the data pipeline

### Manual Docker Commands

```bash
# Build images
docker-compose build

# Start all services
docker-compose up -d

# Start specific services
docker-compose up -d postgres backend frontend

# Run data pipeline
docker-compose --profile pipeline run --rm pipeline

# View logs
docker-compose logs -f backend

# Stop services
docker-compose down

# Remove volumes (warning: deletes data)
docker-compose down -v
```

## Cloud Deployment

### AWS Deployment

#### Using ECS (Elastic Container Service)

1. **Push images to ECR**:
```bash
# Authenticate with ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

# Tag and push images
docker tag datamax-backend:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/datamax-backend:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/datamax-backend:latest
```

2. **Create RDS PostgreSQL instance**
3. **Create ECS cluster and task definitions**
4. **Deploy services to ECS**

#### Using EC2

```bash
# SSH to EC2 instance
ssh -i key.pem ec2-user@<instance-ip>

# Install Docker
sudo yum update -y
sudo yum install docker -y
sudo service docker start

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Clone repository and deploy
git clone <repository-url>
cd Axtria
docker-compose up -d
```

### Azure Deployment

#### Using Azure Container Instances

```bash
# Create resource group
az group create --name datamax-rg --location eastus

# Create Azure Database for PostgreSQL
az postgres server create --resource-group datamax-rg --name datamax-db --location eastus --admin-user postgres --admin-password <password> --sku-name B_Gen5_1

# Create container registry
az acr create --resource-group datamax-rg --name datamaxacr --sku Basic

# Push images and deploy
az acr build --registry datamaxacr --image datamax-backend:latest ./backend
az container create --resource-group datamax-rg --name datamax-backend --image datamaxacr.azurecr.io/datamax-backend:latest
```

### Environment Variables

Create a `.env` file for production:

```env
# Database
DATABASE_URL=postgresql://user:password@host:5432/datamax

# Backend
SECRET_KEY=<generate-secure-key>
ENVIRONMENT=production
LOG_LEVEL=INFO

# Frontend
API_URL=https://api.yourdomain.com/api/v1
```

## CI/CD Pipeline

### GitHub Actions Example

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy DataMAx

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: |
          chmod +x scripts/run-tests.sh
          ./scripts/run-tests.sh

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to production
        run: |
          # Your deployment commands here
```

## Monitoring and Logging

### Using Docker Logs

```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f postgres
```

### Production Monitoring

Consider integrating:
- **Prometheus** for metrics
- **Grafana** for visualization
- **ELK Stack** for log aggregation
- **Sentry** for error tracking

## Backup and Recovery

### Database Backup

```bash
# Create backup
docker-compose exec postgres pg_dump -U postgres datamax > backup.sql

# Restore backup
docker-compose exec -T postgres psql -U postgres datamax < backup.sql
```

## Scaling

### Horizontal Scaling

```bash
# Scale backend service
docker-compose up -d --scale backend=3

# Use load balancer (nginx/haproxy) for distribution
```

## Health Checks

```bash
# Backend health
curl http://localhost:8000/health

# Database connection
docker-compose exec postgres pg_isready -U postgres
```

## Troubleshooting

### Common Issues

1. **Database connection failed**
   - Check if PostgreSQL is running: `docker-compose ps`
   - Verify DATABASE_URL in environment

2. **Frontend can't reach backend**
   - Check CORS settings in backend
   - Verify API_URL in frontend environment

3. **Port already in use**
   - Change ports in docker-compose.yml
   - Or stop conflicting services

### Debug Mode

```bash
# Run backend in debug mode
docker-compose run --rm backend python -m pdb app/main.py

# Access container shell
docker-compose exec backend bash
```
