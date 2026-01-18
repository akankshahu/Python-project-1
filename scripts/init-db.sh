#!/bin/bash

# Database initialization script
# Run database migrations and seed data

set -e

echo "Initializing DataMAx database..."

# Wait for PostgreSQL to be ready
until psql -h postgres -U postgres -d datamax -c '\q' 2>/dev/null; do
  echo "Waiting for PostgreSQL to be ready..."
  sleep 2
done

echo "PostgreSQL is ready"

# Run schema
echo "Creating database schema..."
psql -h postgres -U postgres -d datamax -f /app/database/schema.sql

# Run seed data
echo "Loading seed data..."
psql -h postgres -U postgres -d datamax -f /app/database/seed_data.sql

echo "Database initialization complete!"
