import pandas as pd
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Optional

logger = logging.getLogger(__name__)


class DataLoader:
    """Load transformed data into database"""
    
    def __init__(self, database_url: str):
        """
        Initialize DataLoader
        
        Args:
            database_url: PostgreSQL connection string
        """
        self.engine = create_engine(database_url)
        self.Session = sessionmaker(bind=self.engine)
    
    def load_dataframe(
        self,
        df: pd.DataFrame,
        table_name: str,
        if_exists: str = 'append'
    ) -> bool:
        """
        Load dataframe into database table
        
        Args:
            df: DataFrame to load
            table_name: Target table name
            if_exists: How to behave if table exists ('append', 'replace', 'fail')
            
        Returns:
            Success status
        """
        try:
            logger.info(f"Loading {len(df)} records into table '{table_name}'...")
            
            df.to_sql(
                name=table_name,
                con=self.engine,
                if_exists=if_exists,
                index=False,
                method='multi',
                chunksize=1000
            )
            
            logger.info(f"Successfully loaded data into '{table_name}'")
            return True
            
        except Exception as e:
            logger.error(f"Error loading data into '{table_name}': {str(e)}")
            return False
    
    def load_drugs(self, df: pd.DataFrame) -> bool:
        """Load drug data"""
        # Prepare data for loading
        df_load = df.copy()
        
        # Remove auto-increment columns if present
        if 'id' in df_load.columns:
            df_load = df_load.drop('id', axis=1)
        
        # Convert dates to proper format
        if 'approval_date' in df_load.columns:
            df_load['approval_date'] = pd.to_datetime(df_load['approval_date'], errors='coerce')
        
        return self.load_dataframe(df_load, 'drugs', if_exists='append')
    
    def load_clinical_trials(self, df: pd.DataFrame) -> bool:
        """Load clinical trial data"""
        df_load = df.copy()
        
        if 'id' in df_load.columns:
            df_load = df_load.drop('id', axis=1)
        
        # Convert dates
        for col in ['start_date', 'end_date']:
            if col in df_load.columns:
                df_load[col] = pd.to_datetime(df_load[col], errors='coerce')
        
        return self.load_dataframe(df_load, 'clinical_trials', if_exists='append')
    
    def truncate_table(self, table_name: str) -> bool:
        """
        Truncate a table (useful for reloading data)
        
        Args:
            table_name: Name of table to truncate
            
        Returns:
            Success status
        """
        try:
            with self.engine.connect() as conn:
                conn.execute(f"TRUNCATE TABLE {table_name} CASCADE")
                conn.commit()
            logger.info(f"Truncated table '{table_name}'")
            return True
        except Exception as e:
            logger.error(f"Error truncating table '{table_name}': {str(e)}")
            return False
