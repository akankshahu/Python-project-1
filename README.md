# DataMAx - Pharmaceutical Data Analytics Platform

A multi-cloud pharmaceutical data analytics platform for processing, analyzing, and visualizing clinical trial and drug data.

## 🚀 Project Overview

DataMAx is a full-stack data analytics platform built to demonstrate enterprise-scale data engineering and backend development capabilities. The platform processes pharmaceutical data, provides RESTful APIs for data access, and includes a web interface for data visualization.

## 🏗️ Architecture

### Tech Stack
- **Backend**: Python 3.10+, FastAPI, SQLAlchemy
- **Database**: PostgreSQL
- **Frontend**: Angular 16+
- **Data Processing**: Pandas, NumPy
- **Testing**: pytest, unittest
- **Containerization**: Docker, Docker Compose
- **Cloud**: AWS/Azure compatible architecture

### Components
1. **Backend API** (`/backend`) - RESTful services for data operations
2. **Data Pipeline** (`/data-pipeline`) - ETL workflows for pharmaceutical data
3. **Database** (`/database`) - Schema, migrations, and SQL scripts
4. **Frontend** (`/frontend`) - Angular dashboard for data visualization
5. **Tests** (`/tests`) - Unit and integration tests

## 📋 Features

- ✅ RESTful API for pharmaceutical data operations
- ✅ Data ingestion and processing pipelines
- ✅ Data quality validation and monitoring
- ✅ SQL-based data analytics and reporting
- ✅ Interactive data visualization dashboard
- ✅ Containerized deployment with Docker
- ✅ Comprehensive unit test coverage

## 🔧 Prerequisites

- Python 3.10 or higher
- Node.js 16+ and npm
- PostgreSQL 13+
- Docker and Docker Compose (optional)

## 🚀 Quick Start

### Using Docker (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd Axtria

# Start all services
docker-compose up -d

# Access the application
# Frontend: http://localhost:4200
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Manual Setup

#### 1. Database Setup

```bash
# Start PostgreSQL
sudo systemctl start postgresql

# Create database
psql -U postgres
CREATE DATABASE datamax;
\q

# Run migrations
cd database
psql -U postgres -d datamax -f schema.sql
psql -U postgres -d datamax -f seed_data.sql
```

#### 2. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your database credentials

# Run the backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 3. Frontend Setup

```bash
cd frontend
npm install
ng serve
```

#### 4. Data Pipeline

```bash
cd data-pipeline
pip install -r requirements.txt
python pipeline/main.py --mode full
```

## 📊 API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Key Endpoints

- `GET /api/v1/drugs` - List all drugs
- `GET /api/v1/clinical-trials` - List clinical trials
- `POST /api/v1/data/ingest` - Ingest new data
- `GET /api/v1/analytics/summary` - Get analytics summary
- `GET /api/v1/health` - Health check

## 🧪 Running Tests

```bash
# Backend tests
cd backend
pytest tests/ -v --cov=app

# Integration tests
pytest tests/integration/ -v

# Data pipeline tests
cd data-pipeline
pytest tests/ -v
```

## 📁 Project Structure

```
Axtria/
├── backend/                    # FastAPI backend service
│   ├── app/
│   │   ├── api/               # API routes
│   │   ├── models/            # Database models
│   │   ├── schemas/           # Pydantic schemas
│   │   ├── services/          # Business logic
│   │   ├── db/                # Database connection
│   │   └── main.py            # Application entry point
│   ├── tests/                 # Backend tests
│   └── requirements.txt
├── data-pipeline/             # Data processing workflows
│   ├── pipeline/
│   │   ├── extractors/        # Data extraction
│   │   ├── transformers/      # Data transformation
│   │   ├── loaders/           # Data loading
│   │   └── validators/        # Data quality checks
│   ├── tests/
│   └── requirements.txt
├── database/                  # Database scripts
│   ├── schema.sql            # Table definitions
│   ├── migrations/           # Database migrations
│   ├── queries/              # Common SQL queries
│   └── seed_data.sql         # Sample data
├── frontend/                  # Angular frontend
│   ├── src/
│   │   ├── app/
│   │   │   ├── components/   # UI components
│   │   │   ├── services/     # API services
│   │   │   └── models/       # TypeScript models
│   │   └── assets/
│   └── package.json
├── docker/                    # Docker configurations
│   ├── Dockerfile.backend
│   ├── Dockerfile.frontend
│   └── Dockerfile.pipeline
├── docs/                      # Additional documentation
├── scripts/                   # Utility scripts
├── docker-compose.yml
└── README.md
```

## 🔐 Environment Variables

Create a `.env` file in the backend directory:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/datamax
SECRET_KEY=your-secret-key-here
ENVIRONMENT=development
LOG_LEVEL=INFO
```

## 📈 Data Pipeline Workflow

1. **Extract** - Fetch data from various sources (CSV, APIs, databases)
2. **Transform** - Clean, validate, and enrich pharmaceutical data
3. **Load** - Insert processed data into PostgreSQL
4. **Validate** - Run quality checks and generate reports


## 📝 Key Skills Demonstrated

- ✅ Python OOP, data structures, and algorithms
- ✅ RESTful API design and development
- ✅ SQL and relational database management
- ✅ Data pipeline development
- ✅ Frontend development (Angular)
- ✅ Version control with Git
- ✅ Docker containerization
- ✅ Unit testing with pytest
- ✅ Cloud-native architecture

