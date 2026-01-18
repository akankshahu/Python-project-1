from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas.schemas import AnalyticsSummary
from app.services.services import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/summary", response_model=AnalyticsSummary)
def get_analytics_summary(db: Session = Depends(get_db)):
    """
    Get comprehensive analytics summary
    
    Returns:
    - Total number of drugs
    - Total number of clinical trials
    - Active trials count
    - Completed trials count
    - Total adverse events
    - Distribution of trials by phase
    - Distribution of trials by status
    """
    return AnalyticsService.get_summary(db)


@router.get("/drugs/top-manufacturers")
def get_top_manufacturers(db: Session = Depends(get_db)):
    """
    Get top drug manufacturers by number of drugs
    """
    from sqlalchemy import func
    from app.models.models import Drug
    
    results = db.query(
        Drug.manufacturer,
        func.count(Drug.id).label('count')
    ).group_by(Drug.manufacturer).order_by(func.count(Drug.id).desc()).limit(10).all()
    
    return [{"manufacturer": r[0], "drug_count": r[1]} for r in results if r[0]]


@router.get("/trials/by-therapeutic-area")
def get_trials_by_therapeutic_area(db: Session = Depends(get_db)):
    """
    Get trial distribution by therapeutic area
    """
    from sqlalchemy import func
    from app.models.models import ClinicalTrial, Drug
    
    results = db.query(
        Drug.therapeutic_area,
        func.count(ClinicalTrial.id).label('count')
    ).join(ClinicalTrial, Drug.id == ClinicalTrial.drug_id) \
     .group_by(Drug.therapeutic_area) \
     .order_by(func.count(ClinicalTrial.id).desc()).all()
    
    return [{"therapeutic_area": r[0], "trial_count": r[1]} for r in results if r[0]]
