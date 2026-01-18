import pytest
import pandas as pd
from pipeline.extractors import MockDataExtractor


def test_mock_drug_data_generation():
    """Test mock drug data generation"""
    df = MockDataExtractor.generate_drugs_data()
    
    # Check dataframe properties
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0
    
    # Check required columns
    required_columns = ['name', 'generic_name', 'manufacturer']
    for col in required_columns:
        assert col in df.columns
    
    # Check no null values in critical fields
    assert df['name'].isna().sum() == 0


def test_mock_clinical_trial_data_generation():
    """Test mock clinical trial data generation"""
    df = MockDataExtractor.generate_clinical_trials_data()
    
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0
    
    # Check required columns
    required_columns = ['trial_id', 'title', 'drug_id']
    for col in required_columns:
        assert col in df.columns
    
    # Check trial_id uniqueness
    assert df['trial_id'].is_unique


def test_mock_data_consistency():
    """Test consistency between mock drugs and trials"""
    drugs_df = MockDataExtractor.generate_drugs_data()
    trials_df = MockDataExtractor.generate_clinical_trials_data()
    
    # All trial drug_ids should be valid
    max_drug_id = len(drugs_df)
    assert trials_df['drug_id'].max() <= max_drug_id
    assert trials_df['drug_id'].min() >= 1
