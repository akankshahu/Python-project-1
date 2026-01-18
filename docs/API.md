# DataMAx API Documentation

## Overview

DataMAx provides a RESTful API for managing pharmaceutical data including drugs, clinical trials, and analytics.

**Base URL**: `http://localhost:8000/api/v1`

**Interactive Documentation**: 
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Authentication

Currently, the API does not require authentication. In production, implement JWT tokens or API keys.

## Endpoints

### Health Check

#### GET `/health`

Check API health status.

**Response**:
```json
{
  "status": "healthy",
  "environment": "development"
}
```

---

### Drugs

#### GET `/api/v1/drugs/`

Get all drugs with pagination.

**Query Parameters**:
- `skip` (int): Number of records to skip (default: 0)
- `limit` (int): Maximum records to return (default: 100)

**Response**:
```json
[
  {
    "id": 1,
    "name": "Aspirin",
    "generic_name": "Acetylsalicylic acid",
    "manufacturer": "Bayer",
    "approval_date": "1899-03-06",
    "therapeutic_area": "Cardiology",
    "molecule_type": "Small Molecule",
    "created_at": "2024-01-18T10:00:00",
    "updated_at": "2024-01-18T10:00:00"
  }
]
```

#### GET `/api/v1/drugs/{drug_id}`

Get a specific drug by ID.

**Path Parameters**:
- `drug_id` (int): Drug ID

**Response**: Same as single drug object above

#### POST `/api/v1/drugs/`

Create a new drug.

**Request Body**:
```json
{
  "name": "New Drug",
  "generic_name": "Generic Name",
  "manufacturer": "Pharma Co",
  "therapeutic_area": "Oncology",
  "molecule_type": "Small Molecule"
}
```

**Response**: Created drug object with HTTP 201

#### PUT `/api/v1/drugs/{drug_id}`

Update an existing drug.

**Request Body** (all fields optional):
```json
{
  "name": "Updated Name",
  "manufacturer": "New Manufacturer"
}
```

#### DELETE `/api/v1/drugs/{drug_id}`

Delete a drug. Returns HTTP 204 on success.

---

### Clinical Trials

#### GET `/api/v1/clinical-trials/`

Get all clinical trials.

**Query Parameters**:
- `skip` (int): Number of records to skip
- `limit` (int): Maximum records to return
- `drug_id` (int, optional): Filter by drug ID

**Response**:
```json
[
  {
    "id": 1,
    "trial_id": "NCT00001",
    "title": "Phase 3 Study of Drug X",
    "drug_id": 1,
    "phase": "Phase 3",
    "status": "Ongoing",
    "start_date": "2020-01-15",
    "end_date": null,
    "patient_count": 500,
    "location": "USA",
    "sponsor": "Pharma Corp",
    "created_at": "2024-01-18T10:00:00",
    "updated_at": "2024-01-18T10:00:00"
  }
]
```

#### GET `/api/v1/clinical-trials/{trial_id}`

Get a specific clinical trial.

#### POST `/api/v1/clinical-trials/`

Create a new clinical trial.

**Request Body**:
```json
{
  "trial_id": "NCT12345",
  "title": "New Clinical Trial",
  "drug_id": 1,
  "phase": "Phase 2",
  "status": "Planned",
  "patient_count": 200,
  "location": "USA",
  "sponsor": "Research Institute"
}
```

**Enum Values**:
- `phase`: "Phase 1", "Phase 2", "Phase 3", "Phase 4"
- `status`: "Planned", "Ongoing", "Completed", "Terminated"

#### PUT `/api/v1/clinical-trials/{trial_id}`

Update a clinical trial.

---

### Analytics

#### GET `/api/v1/analytics/summary`

Get comprehensive analytics summary.

**Response**:
```json
{
  "total_drugs": 10,
  "total_trials": 25,
  "active_trials": 8,
  "completed_trials": 15,
  "total_adverse_events": 50,
  "trials_by_phase": {
    "Phase 1": 5,
    "Phase 2": 8,
    "Phase 3": 10,
    "Phase 4": 2
  },
  "trials_by_status": {
    "Planned": 2,
    "Ongoing": 8,
    "Completed": 15,
    "Terminated": 0
  }
}
```

#### GET `/api/v1/analytics/drugs/top-manufacturers`

Get top drug manufacturers.

**Response**:
```json
[
  {
    "manufacturer": "Pfizer",
    "drug_count": 15
  }
]
```

#### GET `/api/v1/analytics/trials/by-therapeutic-area`

Get trial distribution by therapeutic area.

**Response**:
```json
[
  {
    "therapeutic_area": "Oncology",
    "trial_count": 12
  }
]
```

---

## Error Responses

### 404 Not Found
```json
{
  "detail": "Drug not found"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "name"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

---

## Rate Limiting

Currently no rate limiting is implemented. For production, consider:
- 100 requests per minute per IP
- Use Redis for distributed rate limiting

## CORS

CORS is enabled for:
- Frontend: `http://localhost:4200`

For production, update CORS origins in `backend/app/main.py`.

## Pagination

All list endpoints support pagination:
- Default limit: 100
- Maximum limit: 1000
- Use `skip` and `limit` parameters

**Example**:
```
GET /api/v1/drugs/?skip=0&limit=50
```

## Filtering

Some endpoints support filtering:
- Clinical trials by drug: `/api/v1/clinical-trials/?drug_id=1`

## Sorting

Currently not implemented. Future enhancement.

## Code Examples

### Python
```python
import requests

# Get all drugs
response = requests.get('http://localhost:8000/api/v1/drugs/')
drugs = response.json()

# Create a drug
new_drug = {
    "name": "Test Drug",
    "manufacturer": "Test Pharma"
}
response = requests.post('http://localhost:8000/api/v1/drugs/', json=new_drug)
```

### JavaScript/TypeScript
```typescript
// Get analytics summary
fetch('http://localhost:8000/api/v1/analytics/summary')
  .then(response => response.json())
  .then(data => console.log(data));

// Create a drug
fetch('http://localhost:8000/api/v1/drugs/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    name: 'Test Drug',
    manufacturer: 'Test Pharma'
  })
});
```

### cURL
```bash
# Get drugs
curl http://localhost:8000/api/v1/drugs/

# Create drug
curl -X POST http://localhost:8000/api/v1/drugs/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Test Drug","manufacturer":"Test Pharma"}'

# Get analytics
curl http://localhost:8000/api/v1/analytics/summary
```
