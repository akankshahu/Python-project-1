import pytest


def test_create_clinical_trial(client, sample_drug):
    """Test creating a new clinical trial"""
    trial_data = {
        "trial_id": "NCT12345",
        "title": "Test Clinical Trial",
        "drug_id": sample_drug.id,
        "phase": "Phase 3",
        "status": "Ongoing",
        "patient_count": 100,
        "location": "USA",
        "sponsor": "Test Sponsor"
    }
    response = client.post("/api/v1/clinical-trials/", json=trial_data)
    assert response.status_code == 201
    data = response.json()
    assert data["trial_id"] == trial_data["trial_id"]
    assert data["drug_id"] == sample_drug.id


def test_get_trials_empty(client):
    """Test getting trials when database is empty"""
    response = client.get("/api/v1/clinical-trials/")
    assert response.status_code == 200
    assert response.json() == []


def test_get_trial_by_id(client, sample_trial):
    """Test getting a specific trial by ID"""
    response = client.get(f"/api/v1/clinical-trials/{sample_trial.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["trial_id"] == sample_trial.trial_id
    assert data["id"] == sample_trial.id


def test_get_trials_by_drug(client, sample_drug, sample_trial):
    """Test filtering trials by drug ID"""
    response = client.get(f"/api/v1/clinical-trials/?drug_id={sample_drug.id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["drug_id"] == sample_drug.id


def test_update_trial(client, sample_trial):
    """Test updating a clinical trial"""
    update_data = {
        "status": "Completed",
        "patient_count": 150
    }
    response = client.put(f"/api/v1/clinical-trials/{sample_trial.id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "Completed"
    assert data["patient_count"] == 150


def test_trial_not_found(client):
    """Test getting a non-existent trial"""
    response = client.get("/api/v1/clinical-trials/9999")
    assert response.status_code == 404


def test_trial_phase_validation(client, sample_drug):
    """Test trial phase enum validation"""
    trial_data = {
        "trial_id": "NCT99999",
        "title": "Test Trial",
        "drug_id": sample_drug.id,
        "phase": "Phase 3",
        "status": "Ongoing"
    }
    response = client.post("/api/v1/clinical-trials/", json=trial_data)
    assert response.status_code == 201


def test_trial_status_validation(client, sample_drug):
    """Test trial status enum validation"""
    trial_data = {
        "trial_id": "NCT88888",
        "title": "Test Trial",
        "drug_id": sample_drug.id,
        "phase": "Phase 2",
        "status": "Completed"
    }
    response = client.post("/api/v1/clinical-trials/", json=trial_data)
    assert response.status_code == 201
