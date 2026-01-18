#!/bin/bash

# DataMAx Platform Setup Script
# This script sets up the complete DataMAx platform

set -e

echo "=========================================="
echo "DataMAx Platform Setup"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    print_warning "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    print_warning "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

print_success "Docker and Docker Compose are installed"
echo ""

# Build and start services
print_info "Building Docker images..."
docker-compose build

print_success "Docker images built successfully"
echo ""

print_info "Starting services..."
docker-compose up -d postgres backend frontend

print_success "Services started successfully"
echo ""

# Wait for database to be ready
print_info "Waiting for database to be ready..."
sleep 10

# Run data pipeline
print_info "Running data pipeline to populate database..."
docker-compose --profile pipeline run --rm pipeline

print_success "Data pipeline completed"
echo ""

# Display status
print_info "Service status:"
docker-compose ps
echo ""

echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Access the application at:"
echo "  - Frontend: http://localhost:4200"
echo "  - Backend API: http://localhost:8000"
echo "  - API Docs: http://localhost:8000/docs"
echo ""
echo "To stop services:"
echo "  docker-compose down"
echo ""
echo "To view logs:"
echo "  docker-compose logs -f [service-name]"
echo ""
