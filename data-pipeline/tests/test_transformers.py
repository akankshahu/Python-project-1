import pytest
import pandas as pd
from pipeline.transformers import DataTransformer


def test_clean_drug_data():
    """Test drug data cleaning"""
    # Create sample data with issues
    data = {
        'name': ['  aspirin  ', 'IBUPROFEN', 'aspirin', 'Metformin'],
        'generic_name': [None, 'Ibuprofen', 'Aspirin', 'Metformin'],
        'manufacturer': ['Bayer', None, 'Bayer', 'Merck'],
        'approval_date': ['1899-03-06', '1969-01-01', '1899-03-06', 'invalid']
    }
    df = pd.DataFrame(data)
    
    # Clean data
    df_clean = DataTransformer.clean_drug_data(df)
    
    # Assertions
    assert len(df_clean) == 3  # One duplicate removed
    assert df_clean['manufacturer'].isna().sum() == 0  # No null manufacturers
    assert df_clean['name'].str.strip().eq(df_clean['name']).all()  # Names are stripped


def test_clean_clinical_trial_data():
    """Test clinical trial data cleaning"""
    data = {
        'trial_id': ['nct001', 'NCT002', 'nct001'],
        'title': ['Trial 1', 'Trial 2', 'Trial 1 Duplicate'],
        'drug_id': [1, 2, 1],
        'phase': ['phase 1', 'Phase 2', 'phase 1'],
        'status': ['ongoing', 'Completed', 'ongoing'],
        'start_date': ['2020-01-01', '2021-01-01', '2020-01-01'],
        'patient_count': [100, -50, 100]
    }
    df = pd.DataFrame(data)
    
    df_clean = DataTransformer.clean_clinical_trial_data(df)
    
    # Check duplicates removed
    assert len(df_clean) == 2
    
    # Check trial_id standardization
    assert all(df_clean['trial_id'].str.isupper())
    
    # Check phase standardization
    assert 'Phase 1' in df_clean['phase'].values
    
    # Check patient count validation
    assert (df_clean['patient_count'] >= 0).all()


def test_aggregate_trial_metrics():
    """Test trial metrics aggregation"""
    data = {
        'drug_id': [1, 1, 2, 2, 2],
        'trial_id': ['A', 'B', 'C', 'D', 'E'],
        'patient_count': [100, 150, 200, 250, 300],
        'start_date': pd.to_datetime(['2020-01-01', '2020-06-01', '2019-01-01', '2020-01-01', '2021-01-01']),
        'end_date': pd.to_datetime(['2021-01-01', '2022-01-01', '2020-01-01', '2021-01-01', '2022-01-01'])
    }
    df = pd.DataFrame(data)
    
    metrics = DataTransformer.aggregate_trial_metrics(df)
    
    # Check aggregation
    assert len(metrics) == 2  # Two drugs
    assert metrics[metrics['drug_id'] == 1]['total_trials'].values[0] == 2
    assert metrics[metrics['drug_id'] == 2]['total_trials'].values[0] == 3
    assert metrics[metrics['drug_id'] == 1]['total_patients'].values[0] == 250
