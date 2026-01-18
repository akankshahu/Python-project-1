import pandas as pd
import logging
from typing import List, Dict, Tuple

logger = logging.getLogger(__name__)


class DataValidator:
    """Validate data quality and integrity"""
    
    @staticmethod
    def validate_drug_data(df: pd.DataFrame) -> Tuple[bool, List[str]]:
        """
        Validate drug data quality
        
        Args:
            df: Drug dataframe
            
        Returns:
            Tuple of (is_valid, list of issues)
        """
        logger.info("Validating drug data...")
        issues = []
        
        # Check required columns
        required_columns = ['name']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            issues.append(f"Missing required columns: {missing_columns}")
        
        # Check for null values in critical fields
        if 'name' in df.columns:
            null_count = df['name'].isnull().sum()
            if null_count > 0:
                issues.append(f"Found {null_count} null values in 'name' field")
        
        # Check for duplicates
        if 'name' in df.columns:
            duplicate_count = df.duplicated(subset=['name']).sum()
            if duplicate_count > 0:
                issues.append(f"Found {duplicate_count} duplicate drug names")
        
        # Check data types
        if 'approval_date' in df.columns:
            try:
                pd.to_datetime(df['approval_date'], errors='raise')
            except:
                issues.append("Invalid date format in 'approval_date'")
        
        is_valid = len(issues) == 0
        logger.info(f"Drug data validation: {'PASSED' if is_valid else 'FAILED'}")
        
        return is_valid, issues
    
    @staticmethod
    def validate_clinical_trial_data(df: pd.DataFrame) -> Tuple[bool, List[str]]:
        """
        Validate clinical trial data quality
        
        Args:
            df: Clinical trial dataframe
            
        Returns:
            Tuple of (is_valid, list of issues)
        """
        logger.info("Validating clinical trial data...")
        issues = []
        
        # Check required columns
        required_columns = ['trial_id', 'title', 'drug_id']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            issues.append(f"Missing required columns: {missing_columns}")
        
        # Check for null values
        for col in required_columns:
            if col in df.columns:
                null_count = df[col].isnull().sum()
                if null_count > 0:
                    issues.append(f"Found {null_count} null values in '{col}'")
        
        # Check for duplicate trial IDs
        if 'trial_id' in df.columns:
            duplicate_count = df.duplicated(subset=['trial_id']).sum()
            if duplicate_count > 0:
                issues.append(f"Found {duplicate_count} duplicate trial IDs")
        
        # Validate patient count
        if 'patient_count' in df.columns:
            negative_count = (df['patient_count'] < 0).sum()
            if negative_count > 0:
                issues.append(f"Found {negative_count} negative patient counts")
        
        # Validate date logic
        if 'start_date' in df.columns and 'end_date' in df.columns:
            df_dates = df.dropna(subset=['start_date', 'end_date'])
            invalid_dates = (pd.to_datetime(df_dates['end_date']) < pd.to_datetime(df_dates['start_date'])).sum()
            if invalid_dates > 0:
                issues.append(f"Found {invalid_dates} trials where end_date < start_date")
        
        # Validate phase values
        if 'phase' in df.columns:
            valid_phases = ['Phase 1', 'Phase 2', 'Phase 3', 'Phase 4']
            invalid_phases = ~df['phase'].isin(valid_phases + [None])
            if invalid_phases.any():
                issues.append(f"Found {invalid_phases.sum()} invalid phase values")
        
        # Validate status values
        if 'status' in df.columns:
            valid_statuses = ['Planned', 'Ongoing', 'Completed', 'Terminated']
            invalid_statuses = ~df['status'].isin(valid_statuses + [None])
            if invalid_statuses.any():
                issues.append(f"Found {invalid_statuses.sum()} invalid status values")
        
        is_valid = len(issues) == 0
        logger.info(f"Clinical trial data validation: {'PASSED' if is_valid else 'FAILED'}")
        
        return is_valid, issues
    
    @staticmethod
    def generate_quality_report(df: pd.DataFrame, data_type: str) -> Dict:
        """
        Generate comprehensive data quality report
        
        Args:
            df: Input dataframe
            data_type: Type of data (e.g., 'drugs', 'trials')
            
        Returns:
            Quality report dictionary
        """
        logger.info(f"Generating quality report for {data_type}...")
        
        total_records = len(df)
        
        # Calculate missing data
        missing_data = df.isnull().sum()
        missing_percentage = (missing_data / total_records * 100).round(2)
        
        # Count duplicates
        duplicate_count = df.duplicated().sum()
        
        report = {
            'data_type': data_type,
            'total_records': total_records,
            'duplicate_records': int(duplicate_count),
            'missing_data': {
                col: {
                    'count': int(missing_data[col]),
                    'percentage': float(missing_percentage[col])
                }
                for col in df.columns if missing_data[col] > 0
            },
            'completeness_score': float(100 - missing_percentage.mean())
        }
        
        logger.info(f"Quality report generated: Completeness score = {report['completeness_score']:.2f}%")
        
        return report
