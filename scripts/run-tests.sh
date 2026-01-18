#!/bin/bash

# Run all tests for DataMAx platform

set -e

echo "=========================================="
echo "Running DataMAx Test Suite"
echo "=========================================="
echo ""

# Backend tests
echo "Running backend tests..."
cd backend
python -m pytest tests/ -v --cov=app --cov-report=term-missing
cd ..

echo ""

# Data pipeline tests
echo "Running data pipeline tests..."
cd data-pipeline
python -m pytest tests/ -v --cov=pipeline --cov-report=term-missing
cd ..

echo ""
echo "=========================================="
echo "All tests completed!"
echo "=========================================="
