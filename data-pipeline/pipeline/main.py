#!/usr/bin/env python3
"""
DataMAx ETL Pipeline
Main entry point for pharmaceutical data processing pipeline
"""

import argparse
import logging
import sys
from pathlib import Path
from dotenv import load_dotenv
import os

from pipeline.extractors import DataExtractor, MockDataExtractor
from pipeline.transformers import DataTransformer
from pipeline.validators import DataValidator
from pipeline.loaders import DataLoader

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=getattr(logging, os.getenv('LOG_LEVEL', 'INFO')),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('pipeline.log')
    ]
)

logger = logging.getLogger(__name__)


class DataPipeline:
    """Main ETL Pipeline orchestrator"""
    
    def __init__(self, mode: str = 'full', use_mock_data: bool = True):
        """
        Initialize pipeline
        
        Args:
            mode: Pipeline mode ('full', 'extract', 'transform', 'load')
            use_mock_data: Whether to use mock data or read from files
        """
        self.mode = mode
        self.use_mock_data = use_mock_data
        
        # Initialize components
        self.source_path = os.getenv('DATA_SOURCE_PATH', './data/source')
        self.output_path = os.getenv('DATA_OUTPUT_PATH', './data/processed')
        self.database_url = os.getenv('DATABASE_URL')
        
        if not self.database_url:
            logger.warning("DATABASE_URL not set. Loading to database will be skipped.")
        
        # Create directories if they don't exist
        Path(self.output_path).mkdir(parents=True, exist_ok=True)
    
    def extract(self):
        """Extract data from sources"""
        logger.info("=" * 50)
        logger.info("EXTRACTION PHASE")
        logger.info("=" * 50)
        
        if self.use_mock_data:
            logger.info("Using mock data generator...")
            drugs_df = MockDataExtractor.generate_drugs_data()
            trials_df = MockDataExtractor.generate_clinical_trials_data()
        else:
            logger.info(f"Extracting data from {self.source_path}...")
            extractor = DataExtractor(self.source_path)
            drugs_df = extractor.extract_drugs_data()
            trials_df = extractor.extract_clinical_trials_data()
        
        if drugs_df is None or trials_df is None:
            logger.error("Extraction failed")
            return None, None
        
        logger.info(f"Extracted {len(drugs_df)} drugs and {len(trials_df)} clinical trials")
        
        return drugs_df, trials_df
    
    def transform(self, drugs_df, trials_df):
        """Transform and clean data"""
        logger.info("=" * 50)
        logger.info("TRANSFORMATION PHASE")
        logger.info("=" * 50)
        
        # Clean data
        logger.info("Cleaning drug data...")
        drugs_clean = DataTransformer.clean_drug_data(drugs_df)
        
        logger.info("Cleaning clinical trial data...")
        trials_clean = DataTransformer.clean_clinical_trial_data(trials_df)
        
        # Save transformed data
        drugs_output = Path(self.output_path) / 'drugs_transformed.csv'
        trials_output = Path(self.output_path) / 'trials_transformed.csv'
        
        drugs_clean.to_csv(drugs_output, index=False)
        trials_clean.to_csv(trials_output, index=False)
        
        logger.info(f"Transformed data saved to {self.output_path}")
        
        return drugs_clean, trials_clean
    
    def validate(self, drugs_df, trials_df):
        """Validate data quality"""
        logger.info("=" * 50)
        logger.info("VALIDATION PHASE")
        logger.info("=" * 50)
        
        # Validate drugs
        drugs_valid, drugs_issues = DataValidator.validate_drug_data(drugs_df)
        if not drugs_valid:
            logger.warning(f"Drug data validation issues: {drugs_issues}")
        
        # Validate trials
        trials_valid, trials_issues = DataValidator.validate_clinical_trial_data(trials_df)
        if not trials_valid:
            logger.warning(f"Clinical trial data validation issues: {trials_issues}")
        
        # Generate quality reports
        drugs_report = DataValidator.generate_quality_report(drugs_df, 'drugs')
        trials_report = DataValidator.generate_quality_report(trials_df, 'clinical_trials')
        
        logger.info(f"Drug Data Quality: {drugs_report['completeness_score']:.2f}% complete")
        logger.info(f"Clinical Trial Data Quality: {trials_report['completeness_score']:.2f}% complete")
        
        return drugs_valid and trials_valid
    
    def load(self, drugs_df, trials_df):
        """Load data into database"""
        logger.info("=" * 50)
        logger.info("LOADING PHASE")
        logger.info("=" * 50)
        
        if not self.database_url:
            logger.warning("DATABASE_URL not set. Skipping database load.")
            return False
        
        try:
            loader = DataLoader(self.database_url)
            
            # Load drugs
            logger.info("Loading drug data...")
            drugs_success = loader.load_drugs(drugs_df)
            
            # Load clinical trials
            logger.info("Loading clinical trial data...")
            trials_success = loader.load_clinical_trials(trials_df)
            
            if drugs_success and trials_success:
                logger.info("Data successfully loaded into database")
                return True
            else:
                logger.error("Some data failed to load")
                return False
                
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            return False
    
    def run(self):
        """Run the complete pipeline"""
        logger.info("Starting DataMAx ETL Pipeline")
        logger.info(f"Mode: {self.mode}")
        
        try:
            # Extract
            if self.mode in ['full', 'extract']:
                drugs_df, trials_df = self.extract()
                if drugs_df is None:
                    return False
            
            # Transform
            if self.mode in ['full', 'transform']:
                drugs_df, trials_df = self.transform(drugs_df, trials_df)
            
            # Validate
            if self.mode in ['full', 'validate']:
                is_valid = self.validate(drugs_df, trials_df)
                if not is_valid:
                    logger.warning("Data validation found issues, but continuing...")
            
            # Load
            if self.mode in ['full', 'load']:
                self.load(drugs_df, trials_df)
            
            logger.info("=" * 50)
            logger.info("PIPELINE COMPLETED SUCCESSFULLY")
            logger.info("=" * 50)
            return True
            
        except Exception as e:
            logger.error(f"Pipeline failed: {str(e)}", exc_info=True)
            return False


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='DataMAx ETL Pipeline')
    parser.add_argument(
        '--mode',
        choices=['full', 'extract', 'transform', 'validate', 'load'],
        default='full',
        help='Pipeline execution mode'
    )
    parser.add_argument(
        '--use-files',
        action='store_true',
        help='Use CSV files instead of mock data'
    )
    
    args = parser.parse_args()
    
    # Run pipeline
    pipeline = DataPipeline(mode=args.mode, use_mock_data=not args.use_files)
    success = pipeline.run()
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
