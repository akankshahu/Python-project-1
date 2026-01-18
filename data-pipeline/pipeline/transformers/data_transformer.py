import pandas as pd
import numpy as np
import logging
from typing import Optional, List, Dict

logger = logging.getLogger(__name__)


class DataTransformer:
    """Transform and clean pharmaceutical data"""
    
    @staticmethod
    def clean_drug_data(df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and standardize drug data
        
        Args:
            df: Raw drug dataframe
            
        Returns:
            Cleaned dataframe
        """
        logger.info("Cleaning drug data...")
        
        # Create a copy to avoid modifying original
        df_clean = df.copy()
        
        # Remove duplicates
        df_clean = df_clean.drop_duplicates(subset=['name'], keep='first')
        
        # Handle missing values
        df_clean['generic_name'] = df_clean['generic_name'].fillna(df_clean['name'])
        df_clean['manufacturer'] = df_clean['manufacturer'].fillna('Unknown')
        
        # Standardize text fields
        df_clean['name'] = df_clean['name'].str.strip().str.title()
        df_clean['manufacturer'] = df_clean['manufacturer'].str.strip()
        
        # Convert dates
        if 'approval_date' in df_clean.columns:
            df_clean['approval_date'] = pd.to_datetime(df_clean['approval_date'], errors='coerce')
        
        logger.info(f"Cleaned drug data: {len(df_clean)} records")
        return df_clean
    
    @staticmethod
    def clean_clinical_trial_data(df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and standardize clinical trial data
        
        Args:
            df: Raw clinical trial dataframe
            
        Returns:
            Cleaned dataframe
        """
        logger.info("Cleaning clinical trial data...")
        
        df_clean = df.copy()
        
        # Remove duplicates based on trial_id
        df_clean = df_clean.drop_duplicates(subset=['trial_id'], keep='first')
        
        # Standardize trial_id format
        df_clean['trial_id'] = df_clean['trial_id'].str.upper().str.strip()
        
        # Convert dates
        date_columns = ['start_date', 'end_date']
        for col in date_columns:
            if col in df_clean.columns:
                df_clean[col] = pd.to_datetime(df_clean[col], errors='coerce')
        
        # Validate patient_count
        if 'patient_count' in df_clean.columns:
            df_clean['patient_count'] = pd.to_numeric(df_clean['patient_count'], errors='coerce')
            df_clean['patient_count'] = df_clean['patient_count'].clip(lower=0)
        
        # Standardize enum values
        if 'phase' in df_clean.columns:
            phase_mapping = {
                'phase 1': 'Phase 1',
                'phase 2': 'Phase 2',
                'phase 3': 'Phase 3',
                'phase 4': 'Phase 4',
                'phase i': 'Phase 1',
                'phase ii': 'Phase 2',
                'phase iii': 'Phase 3',
                'phase iv': 'Phase 4'
            }
            df_clean['phase'] = df_clean['phase'].str.lower().map(phase_mapping).fillna(df_clean['phase'])
        
        if 'status' in df_clean.columns:
            status_mapping = {
                'planned': 'Planned',
                'ongoing': 'Ongoing',
                'active': 'Ongoing',
                'completed': 'Completed',
                'terminated': 'Terminated',
                'stopped': 'Terminated'
            }
            df_clean['status'] = df_clean['status'].str.lower().map(status_mapping).fillna(df_clean['status'])
        
        logger.info(f"Cleaned clinical trial data: {len(df_clean)} records")
        return df_clean
    
    @staticmethod
    def enrich_data(df: pd.DataFrame, enrichment_fields: Dict) -> pd.DataFrame:
        """
        Enrich data with additional computed fields
        
        Args:
            df: Input dataframe
            enrichment_fields: Dictionary of fields to add
            
        Returns:
            Enriched dataframe
        """
        logger.info("Enriching data...")
        
        df_enriched = df.copy()
        
        for field_name, field_value in enrichment_fields.items():
            df_enriched[field_name] = field_value
        
        return df_enriched
    
    @staticmethod
    def aggregate_trial_metrics(df: pd.DataFrame) -> pd.DataFrame:
        """
        Aggregate clinical trial metrics by drug
        
        Args:
            df: Clinical trials dataframe
            
        Returns:
            Aggregated metrics
        """
        logger.info("Aggregating trial metrics...")
        
        if 'drug_id' not in df.columns:
            logger.warning("No drug_id column found for aggregation")
            return df
        
        metrics = df.groupby('drug_id').agg({
            'trial_id': 'count',
            'patient_count': 'sum',
            'start_date': 'min',
            'end_date': 'max'
        }).reset_index()
        
        metrics.columns = ['drug_id', 'total_trials', 'total_patients', 'first_trial_date', 'last_trial_date']
        
        return metrics
