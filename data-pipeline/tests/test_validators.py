import pytest
import pandas as pd
from pipeline.validators import DataValidator


def test_validate_drug_data_valid():
    """Test validation with valid drug data"""
    data = {
        'name': ['Aspirin', 'Ibuprofen'],
        'manufacturer': ['Bayer', 'Pfizer'],
        'approval_date': ['1899-03-06', '1969-01-01']
    }
    df = pd.DataFrame(data)
    
    is_valid, issues = DataValidator.validate_drug_data(df)
    
    assert is_valid
    assert len(issues) == 0


def test_validate_drug_data_missing_name():
    """Test validation with missing drug names"""
    data = {
        'name': ['Aspirin', None, 'Metformin'],
        'manufacturer': ['Bayer', 'Pfizer', 'Merck']
    }
    df = pd.DataFrame(data)
    
    is_valid, issues = DataValidator.validate_drug_data(df)
    
    assert not is_valid
    assert any('null values' in issue for issue in issues)


def test_validate_drug_data_duplicates():
    """Test validation with duplicate drug names"""
    data = {
        'name': ['Aspirin', 'Aspirin', 'Metformin'],
        'manufacturer': ['Bayer', 'Generic', 'Merck']
    }
    df = pd.DataFrame(data)
    
    is_valid, issues = DataValidator.validate_drug_data(df)
    
    assert not is_valid
    assert any('duplicate' in issue.lower() for issue in issues)


def test_validate_clinical_trial_data_valid():
    """Test validation with valid trial data"""
    data = {
        'trial_id': ['NCT001', 'NCT002'],
        'title': ['Trial 1', 'Trial 2'],
        'drug_id': [1, 2],
        'phase': ['Phase 1', 'Phase 2'],
        'status': ['Ongoing', 'Completed'],
        'patient_count': [100, 200],
        'start_date': ['2020-01-01', '2021-01-01'],
        'end_date': ['2022-01-01', '2023-01-01']
    }
    df = pd.DataFrame(data)
    
    is_valid, issues = DataValidator.validate_clinical_trial_data(df)
    
    assert is_valid
    assert len(issues) == 0


def test_validate_clinical_trial_invalid_dates():
    """Test validation with invalid date logic"""
    data = {
        'trial_id': ['NCT001'],
        'title': ['Trial 1'],
        'drug_id': [1],
        'start_date': ['2022-01-01'],
        'end_date': ['2020-01-01']  # End before start
    }
    df = pd.DataFrame(data)
    
    is_valid, issues = DataValidator.validate_clinical_trial_data(df)
    
    assert not is_valid
    assert any('end_date' in issue for issue in issues)


def test_validate_clinical_trial_negative_patients():
    """Test validation with negative patient count"""
    data = {
        'trial_id': ['NCT001'],
        'title': ['Trial 1'],
        'drug_id': [1],
        'patient_count': [-100]
    }
    df = pd.DataFrame(data)
    
    is_valid, issues = DataValidator.validate_clinical_trial_data(df)
    
    assert not is_valid
    assert any('negative' in issue.lower() for issue in issues)


def test_generate_quality_report():
    """Test quality report generation"""
    data = {
        'name': ['Drug1', 'Drug2', None],
        'manufacturer': ['Pharma1', None, 'Pharma3'],
        'approval_date': ['2020-01-01', '2021-01-01', '2022-01-01']
    }
    df = pd.DataFrame(data)
    
    report = DataValidator.generate_quality_report(df, 'drugs')
    
    assert report['data_type'] == 'drugs'
    assert report['total_records'] == 3
    assert 'missing_data' in report
    assert 'completeness_score' in report
    assert report['completeness_score'] < 100  # Has missing data
