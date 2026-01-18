from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional, List
from enum import Enum


class TrialPhaseEnum(str, Enum):
    PHASE_1 = "Phase 1"
    PHASE_2 = "Phase 2"
    PHASE_3 = "Phase 3"
    PHASE_4 = "Phase 4"


class TrialStatusEnum(str, Enum):
    PLANNED = "Planned"
    ONGOING = "Ongoing"
    COMPLETED = "Completed"
    TERMINATED = "Terminated"


# Drug Schemas
class DrugBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    generic_name: Optional[str] = None
    manufacturer: Optional[str] = None
    approval_date: Optional[date] = None
    therapeutic_area: Optional[str] = None
    molecule_type: Optional[str] = None


class DrugCreate(DrugBase):
    pass


class DrugUpdate(BaseModel):
    name: Optional[str] = None
    generic_name: Optional[str] = None
    manufacturer: Optional[str] = None
    approval_date: Optional[date] = None
    therapeutic_area: Optional[str] = None
    molecule_type: Optional[str] = None


class DrugResponse(DrugBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Clinical Trial Schemas
class ClinicalTrialBase(BaseModel):
    trial_id: str = Field(..., min_length=1, max_length=50)
    title: str = Field(..., min_length=1, max_length=500)
    drug_id: int
    phase: TrialPhaseEnum
    status: TrialStatusEnum
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    patient_count: Optional[int] = None
    location: Optional[str] = None
    sponsor: Optional[str] = None


class ClinicalTrialCreate(ClinicalTrialBase):
    pass


class ClinicalTrialUpdate(BaseModel):
    title: Optional[str] = None
    phase: Optional[TrialPhaseEnum] = None
    status: Optional[TrialStatusEnum] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    patient_count: Optional[int] = None
    location: Optional[str] = None
    sponsor: Optional[str] = None


class ClinicalTrialResponse(ClinicalTrialBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Trial Result Schemas
class TrialResultBase(BaseModel):
    trial_id: int
    endpoint: str
    result_value: Optional[float] = None
    unit: Optional[str] = None
    p_value: Optional[float] = None
    confidence_interval: Optional[str] = None
    notes: Optional[str] = None


class TrialResultCreate(TrialResultBase):
    pass


class TrialResultResponse(TrialResultBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Adverse Event Schemas
class AdverseEventBase(BaseModel):
    drug_id: int
    event_type: str
    severity: str
    frequency: Optional[int] = None
    description: Optional[str] = None
    reported_date: Optional[date] = None


class AdverseEventCreate(AdverseEventBase):
    pass


class AdverseEventResponse(AdverseEventBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Analytics Schemas
class AnalyticsSummary(BaseModel):
    total_drugs: int
    total_trials: int
    active_trials: int
    completed_trials: int
    total_adverse_events: int
    trials_by_phase: dict
    trials_by_status: dict


class DataQualityReport(BaseModel):
    total_records: int
    records_with_issues: int
    missing_data_percentage: float
    duplicate_records: int
    issues: List[str]
