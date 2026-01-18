# Database Setup Guide

## Quick Start

### 1. Create Database

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE datamax;

# Create user (optional)
CREATE USER datamax_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE datamax TO datamax_user;

\q
```

### 2. Initialize Schema

```bash
# Run schema creation
psql -U postgres -d datamax -f schema.sql
```

### 3. Load Sample Data

```bash
# Load seed data
psql -U postgres -d datamax -f seed_data.sql
```

### 4. Verify Installation

```bash
# Connect to database
psql -U postgres -d datamax

# Check tables
\dt

# Check data
SELECT COUNT(*) FROM drugs;
SELECT COUNT(*) FROM clinical_trials;
```

## Database Structure

### Tables

- **drugs**: Pharmaceutical drugs and medications
- **clinical_trials**: Clinical trial information
- **trial_results**: Results and outcomes from trials
- **adverse_events**: Reported adverse events

### Relationships

```
drugs (1) ----< (N) clinical_trials
drugs (1) ----< (N) adverse_events
clinical_trials (1) ----< (N) trial_results
```

## Sample Queries

See `queries/common_queries.sql` for useful queries.

## Migrations

For schema changes, create migration files in `migrations/` directory:

```
migrations/
├── 001_initial_schema.sql
├── 002_add_indexes.sql
└── 003_add_constraints.sql
```
