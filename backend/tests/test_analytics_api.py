import pytest


def test_get_analytics_summary_empty(client):
    """Test analytics summary with empty database"""
    response = client.get("/api/v1/analytics/summary")
    assert response.status_code == 200
    data = response.json()
    assert data["total_drugs"] == 0
    assert data["total_trials"] == 0
    assert data["active_trials"] == 0


def test_get_analytics_summary_with_data(client, sample_drug, sample_trial):
    """Test analytics summary with data"""
    response = client.get("/api/v1/analytics/summary")
    assert response.status_code == 200
    data = response.json()
    assert data["total_drugs"] == 1
    assert data["total_trials"] == 1
    assert data["active_trials"] == 1
    assert "trials_by_phase" in data
    assert "trials_by_status" in data


def test_get_top_manufacturers(client, sample_drug):
    """Test getting top manufacturers"""
    response = client.get("/api/v1/analytics/drugs/top-manufacturers")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_trials_by_therapeutic_area(client, sample_drug, sample_trial):
    """Test getting trial distribution by therapeutic area"""
    response = client.get("/api/v1/analytics/trials/by-therapeutic-area")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if len(data) > 0:
        assert "therapeutic_area" in data[0]
        assert "trial_count" in data[0]
