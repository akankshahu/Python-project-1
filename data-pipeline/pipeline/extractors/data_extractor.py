import pandas as pd
import logging
from typing import Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class DataExtractor:
    """Extract data from various sources"""
    
    def __init__(self, source_path: str):
        self.source_path = Path(source_path)
        
    def extract_from_csv(self, filename: str) -> Optional[pd.DataFrame]:
        """
        Extract data from CSV file
        
        Args:
            filename: Name of the CSV file
            
        Returns:
            DataFrame containing the extracted data
        """
        try:
            file_path = self.source_path / filename
            logger.info(f"Extracting data from {file_path}")
            
            df = pd.read_csv(file_path)
            logger.info(f"Successfully extracted {len(df)} records from {filename}")
            
            return df
            
        except FileNotFoundError:
            logger.error(f"File not found: {file_path}")
            return None
        except Exception as e:
            logger.error(f"Error extracting data from {filename}: {str(e)}")
            return None
    
    def extract_drugs_data(self) -> Optional[pd.DataFrame]:
        """Extract drug data"""
        return self.extract_from_csv("drugs.csv")
    
    def extract_clinical_trials_data(self) -> Optional[pd.DataFrame]:
        """Extract clinical trials data"""
        return self.extract_from_csv("clinical_trials.csv")
    
    def extract_adverse_events_data(self) -> Optional[pd.DataFrame]:
        """Extract adverse events data"""
        return self.extract_from_csv("adverse_events.csv")


class MockDataExtractor:
    """Mock extractor for generating sample data"""
    
    @staticmethod
    def generate_drugs_data() -> pd.DataFrame:
        """Generate sample drug data"""
        data = {
            'name': ['Aspirin', 'Ibuprofen', 'Paracetamol', 'Amoxicillin', 'Metformin'],
            'generic_name': ['Acetylsalicylic acid', 'Ibuprofen', 'Acetaminophen', 'Amoxicillin', 'Metformin'],
            'manufacturer': ['Bayer', 'Pfizer', 'GSK', 'Novartis', 'Merck'],
            'approval_date': ['1899-03-06', '1969-01-01', '1950-01-01', '1972-06-01', '1994-12-29'],
            'therapeutic_area': ['Cardiology', 'Pain Management', 'Pain Management', 'Infectious Disease', 'Endocrinology'],
            'molecule_type': ['Small Molecule', 'Small Molecule', 'Small Molecule', 'Small Molecule', 'Small Molecule']
        }
        return pd.DataFrame(data)
    
    @staticmethod
    def generate_clinical_trials_data() -> pd.DataFrame:
        """Generate sample clinical trial data"""
        data = {
            'trial_id': ['NCT001', 'NCT002', 'NCT003', 'NCT004', 'NCT005'],
            'title': [
                'Phase 3 Study of Aspirin in CAD',
                'Safety Study of Ibuprofen',
                'Efficacy Trial of Paracetamol',
                'Amoxicillin Resistance Study',
                'Metformin in Type 2 Diabetes'
            ],
            'drug_id': [1, 2, 3, 4, 5],
            'phase': ['Phase 3', 'Phase 2', 'Phase 3', 'Phase 4', 'Phase 3'],
            'status': ['Completed', 'Ongoing', 'Completed', 'Ongoing', 'Completed'],
            'start_date': ['2020-01-15', '2021-06-01', '2019-03-20', '2022-01-10', '2018-11-05'],
            'end_date': ['2022-12-31', None, '2021-09-15', None, '2021-08-20'],
            'patient_count': [500, 250, 300, 150, 800],
            'location': ['USA', 'EU', 'USA', 'Asia', 'Global'],
            'sponsor': ['Bayer', 'Pfizer', 'GSK', 'Novartis', 'Merck']
        }
        return pd.DataFrame(data)
