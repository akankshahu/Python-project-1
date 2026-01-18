import pytest
from datetime import date


def test_get_drugs_empty(client):
    """Test getting drugs when database is empty"""
    response = client.get("/api/v1/drugs/")
    assert response.status_code == 200
    assert response.json() == []


def test_create_drug(client):
    """Test creating a new drug"""
    drug_data = {
        "name": "Test Drug",
        "generic_name": "Test Generic",
        "manufacturer": "Test Pharma",
        "therapeutic_area": "Oncology",
        "molecule_type": "Small Molecule"
    }
    response = client.post("/api/v1/drugs/", json=drug_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == drug_data["name"]
    assert data["manufacturer"] == drug_data["manufacturer"]
    assert "id" in data


def test_get_drug_by_id(client, sample_drug):
    """Test getting a specific drug by ID"""
    response = client.get(f"/api/v1/drugs/{sample_drug.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == sample_drug.name
    assert data["id"] == sample_drug.id


def test_get_drug_not_found(client):
    """Test getting a non-existent drug"""
    response = client.get("/api/v1/drugs/9999")
    assert response.status_code == 404


def test_update_drug(client, sample_drug):
    """Test updating a drug"""
    update_data = {
        "manufacturer": "Updated Pharma"
    }
    response = client.put(f"/api/v1/drugs/{sample_drug.id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["manufacturer"] == "Updated Pharma"
    assert data["name"] == sample_drug.name


def test_delete_drug(client, sample_drug):
    """Test deleting a drug"""
    response = client.delete(f"/api/v1/drugs/{sample_drug.id}")
    assert response.status_code == 204
    
    # Verify drug is deleted
    get_response = client.get(f"/api/v1/drugs/{sample_drug.id}")
    assert get_response.status_code == 404


def test_get_multiple_drugs(client):
    """Test getting multiple drugs"""
    # Create multiple drugs
    drugs = [
        {"name": f"Drug {i}", "manufacturer": f"Pharma {i}"}
        for i in range(5)
    ]
    for drug_data in drugs:
        client.post("/api/v1/drugs/", json=drug_data)
    
    response = client.get("/api/v1/drugs/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5


def test_pagination(client):
    """Test drug list pagination"""
    # Create 15 drugs
    for i in range(15):
        client.post("/api/v1/drugs/", json={"name": f"Drug {i}"})
    
    # Get first page
    response = client.get("/api/v1/drugs/?skip=0&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 10
    
    # Get second page
    response = client.get("/api/v1/drugs/?skip=10&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5
