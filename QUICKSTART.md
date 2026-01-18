# DataMAx Platform - Quick Start Guide

## 🚀 System is Running!

All services are currently up and running:

### Service Status
- ✅ **PostgreSQL Database** - Running on port 5432
- ✅ **Backend API** - Running on port 8000
- ✅ **Frontend** - Running on port 4200

## 🌐 Access Points

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://localhost:4200 | Angular web application |
| **Backend API** | http://localhost:8000 | FastAPI REST API |
| **API Docs** | http://localhost:8000/docs | Swagger/OpenAPI documentation |
| **Database** | localhost:5432 | PostgreSQL (user: postgres, pass: password) |

## 📋 Quick Commands

### View Service Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres
```

### Stop Services
```bash
docker-compose down
```

### Restart Services
```bash
docker-compose restart
```

### Rebuild After Code Changes
```bash
# Rebuild and restart
docker-compose up -d --build

# Rebuild specific service
docker-compose up -d --build backend
```

## 🧪 Test the API

```bash
# Health check
curl http://localhost:8000/health

# Get drugs list
curl http://localhost:8000/api/v1/drugs/

# Get clinical trials
curl http://localhost:8000/api/v1/clinical-trials/

# Get analytics summary
curl http://localhost:8000/api/v1/analytics/summary
```

## 🔧 Run Data Pipeline

The data pipeline is configured but not running by default. To execute it:

```bash
# Run the full pipeline
docker-compose --profile pipeline up pipeline

# Run in detached mode
docker-compose --profile pipeline up -d pipeline

# View pipeline logs
docker-compose logs pipeline
```

## 🧹 Clean Up

```bash
# Stop and remove containers, networks
docker-compose down

# Remove volumes (deletes database data)
docker-compose down -v

# Remove images
docker-compose down --rmi all
```

## 📊 Database Access

Connect to PostgreSQL:
```bash
# Using docker exec
docker exec -it datamax-postgres psql -U postgres -d datamax

# Using local psql client
psql -h localhost -U postgres -d datamax
# Password: password
```

## 🛠️ Development Mode

To enable hot-reload for development:

### Backend
The backend is already configured with `--reload` flag in docker-compose.yml

### Frontend
For development with hot-reload:
```bash
cd frontend
npm install
npm start
# Access at http://localhost:4200
```

## 🚨 Troubleshooting

### Port Already in Use
If ports 4200, 8000, or 5432 are in use:
```bash
# Check what's using the port
lsof -i :4200
lsof -i :8000
lsof -i :5432

# Kill process or modify docker-compose.yml ports
```

### Container Won't Start
```bash
# Check logs
docker-compose logs [service-name]

# Rebuild from scratch
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

### Database Not Initialized
```bash
# Restart database to reinitialize
docker-compose down postgres
docker-compose up -d postgres
```

## 📦 Project Structure

```
├── backend/          # FastAPI application
├── frontend/         # Angular application
├── data-pipeline/    # ETL pipeline
├── database/         # SQL schemas and seed data
├── docker/           # Dockerfiles and nginx config
├── scripts/          # Utility scripts
└── docs/             # Documentation
```

## 🎯 Next Steps

1. **Explore API**: Visit http://localhost:8000/docs for interactive API documentation
2. **Use Frontend**: Open http://localhost:4200 to use the web interface
3. **Run Tests**: Execute `./scripts/run-tests.sh` to run the test suite
4. **Customize**: Modify configurations in docker-compose.yml or environment files

---

**Need Help?** Check the main [README.md](README.md) or API documentation in [docs/API.md](docs/API.md)
