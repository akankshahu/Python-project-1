from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.models import Drug, ClinicalTrial, TrialResult, AdverseEvent, TrialStatus
from app.schemas.schemas import (
    DrugCreate, DrugUpdate,
    ClinicalTrialCreate, ClinicalTrialUpdate,
    TrialResultCreate, AdverseEventCreate,
    AnalyticsSummary
)
from datetime import datetime


class DrugService:
    """Service layer for Drug operations"""
    
    @staticmethod
    def get_all_drugs(db: Session, skip: int = 0, limit: int = 100) -> List[Drug]:
        """Get all drugs with pagination"""
        return db.query(Drug).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_drug_by_id(db: Session, drug_id: int) -> Optional[Drug]:
        """Get a specific drug by ID"""
        return db.query(Drug).filter(Drug.id == drug_id).first()
    
    @staticmethod
    def create_drug(db: Session, drug: DrugCreate) -> Drug:
        """Create a new drug"""
        db_drug = Drug(**drug.model_dump())
        db.add(db_drug)
        db.commit()
        db.refresh(db_drug)
        return db_drug
    
    @staticmethod
    def update_drug(db: Session, drug_id: int, drug: DrugUpdate) -> Optional[Drug]:
        """Update an existing drug"""
        db_drug = db.query(Drug).filter(Drug.id == drug_id).first()
        if db_drug:
            update_data = drug.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_drug, key, value)
            db_drug.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(db_drug)
        return db_drug
    
    @staticmethod
    def delete_drug(db: Session, drug_id: int) -> bool:
        """Delete a drug"""
        db_drug = db.query(Drug).filter(Drug.id == drug_id).first()
        if db_drug:
            db.delete(db_drug)
            db.commit()
            return True
        return False


class ClinicalTrialService:
    """Service layer for Clinical Trial operations"""
    
    @staticmethod
    def get_all_trials(db: Session, skip: int = 0, limit: int = 100) -> List[ClinicalTrial]:
        """Get all clinical trials with pagination"""
        return db.query(ClinicalTrial).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_trial_by_id(db: Session, trial_id: int) -> Optional[ClinicalTrial]:
        """Get a specific trial by ID"""
        return db.query(ClinicalTrial).filter(ClinicalTrial.id == trial_id).first()
    
    @staticmethod
    def get_trials_by_drug(db: Session, drug_id: int) -> List[ClinicalTrial]:
        """Get all trials for a specific drug"""
        return db.query(ClinicalTrial).filter(ClinicalTrial.drug_id == drug_id).all()
    
    @staticmethod
    def create_trial(db: Session, trial: ClinicalTrialCreate) -> ClinicalTrial:
        """Create a new clinical trial"""
        db_trial = ClinicalTrial(**trial.model_dump())
        db.add(db_trial)
        db.commit()
        db.refresh(db_trial)
        return db_trial
    
    @staticmethod
    def update_trial(db: Session, trial_id: int, trial: ClinicalTrialUpdate) -> Optional[ClinicalTrial]:
        """Update an existing trial"""
        db_trial = db.query(ClinicalTrial).filter(ClinicalTrial.id == trial_id).first()
        if db_trial:
            update_data = trial.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_trial, key, value)
            db_trial.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(db_trial)
        return db_trial


class AnalyticsService:
    """Service layer for Analytics operations"""
    
    @staticmethod
    def get_summary(db: Session) -> AnalyticsSummary:
        """Get analytics summary"""
        total_drugs = db.query(Drug).count()
        total_trials = db.query(ClinicalTrial).count()
        active_trials = db.query(ClinicalTrial).filter(
            ClinicalTrial.status == TrialStatus.ONGOING
        ).count()
        completed_trials = db.query(ClinicalTrial).filter(
            ClinicalTrial.status == TrialStatus.COMPLETED
        ).count()
        total_adverse_events = db.query(AdverseEvent).count()
        
        # Trials by phase
        from sqlalchemy import func
        trials_by_phase = dict(
            db.query(ClinicalTrial.phase, func.count(ClinicalTrial.id))
            .group_by(ClinicalTrial.phase)
            .all()
        )
        
        # Trials by status
        trials_by_status = dict(
            db.query(ClinicalTrial.status, func.count(ClinicalTrial.id))
            .group_by(ClinicalTrial.status)
            .all()
        )
        
        return AnalyticsSummary(
            total_drugs=total_drugs,
            total_trials=total_trials,
            active_trials=active_trials,
            completed_trials=completed_trials,
            total_adverse_events=total_adverse_events,
            trials_by_phase={str(k): v for k, v in trials_by_phase.items()},
            trials_by_status={str(k): v for k, v in trials_by_status.items()}
        )


class TrialResultService:
    """Service layer for Trial Result operations"""
    
    @staticmethod
    def create_result(db: Session, result: TrialResultCreate) -> TrialResult:
        """Create a new trial result"""
        db_result = TrialResult(**result.model_dump())
        db.add(db_result)
        db.commit()
        db.refresh(db_result)
        return db_result
    
    @staticmethod
    def get_results_by_trial(db: Session, trial_id: int) -> List[TrialResult]:
        """Get all results for a specific trial"""
        return db.query(TrialResult).filter(TrialResult.trial_id == trial_id).all()


class AdverseEventService:
    """Service layer for Adverse Event operations"""
    
    @staticmethod
    def create_event(db: Session, event: AdverseEventCreate) -> AdverseEvent:
        """Create a new adverse event"""
        db_event = AdverseEvent(**event.model_dump())
        db.add(db_event)
        db.commit()
        db.refresh(db_event)
        return db_event
    
    @staticmethod
    def get_events_by_drug(db: Session, drug_id: int) -> List[AdverseEvent]:
        """Get all adverse events for a specific drug"""
        return db.query(AdverseEvent).filter(AdverseEvent.drug_id == drug_id).all()
