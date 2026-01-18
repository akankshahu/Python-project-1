from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db import get_db
from app.schemas.schemas import ClinicalTrialCreate, ClinicalTrialUpdate, ClinicalTrialResponse
from app.services.services import ClinicalTrialService

router = APIRouter(prefix="/clinical-trials", tags=["clinical-trials"])


@router.get("/", response_model=List[ClinicalTrialResponse])
def get_trials(
    skip: int = 0,
    limit: int = 100,
    drug_id: Optional[int] = Query(None, description="Filter by drug ID"),
    db: Session = Depends(get_db)
):
    """
    Get all clinical trials with optional filtering
    
    - **skip**: Number of records to skip
    - **limit**: Maximum number of records to return
    - **drug_id**: Filter trials by drug ID (optional)
    """
    if drug_id:
        trials = ClinicalTrialService.get_trials_by_drug(db, drug_id)
    else:
        trials = ClinicalTrialService.get_all_trials(db, skip=skip, limit=limit)
    return trials


@router.get("/{trial_id}", response_model=ClinicalTrialResponse)
def get_trial(trial_id: int, db: Session = Depends(get_db)):
    """
    Get a specific clinical trial by ID
    
    - **trial_id**: The ID of the trial to retrieve
    """
    trial = ClinicalTrialService.get_trial_by_id(db, trial_id)
    if not trial:
        raise HTTPException(status_code=404, detail="Clinical trial not found")
    return trial


@router.post("/", response_model=ClinicalTrialResponse, status_code=status.HTTP_201_CREATED)
def create_trial(trial: ClinicalTrialCreate, db: Session = Depends(get_db)):
    """
    Create a new clinical trial
    
    - **trial_id**: Unique trial identifier (e.g., NCT12345678)
    - **title**: Trial title
    - **drug_id**: Associated drug ID
    - **phase**: Trial phase (Phase 1, 2, 3, or 4)
    - **status**: Trial status (Planned, Ongoing, Completed, Terminated)
    - **start_date**: Trial start date
    - **end_date**: Trial end date
    - **patient_count**: Number of patients enrolled
    - **location**: Trial location
    - **sponsor**: Trial sponsor organization
    """
    return ClinicalTrialService.create_trial(db, trial)


@router.put("/{trial_id}", response_model=ClinicalTrialResponse)
def update_trial(trial_id: int, trial: ClinicalTrialUpdate, db: Session = Depends(get_db)):
    """
    Update an existing clinical trial
    
    - **trial_id**: The ID of the trial to update
    """
    updated_trial = ClinicalTrialService.update_trial(db, trial_id, trial)
    if not updated_trial:
        raise HTTPException(status_code=404, detail="Clinical trial not found")
    return updated_trial
