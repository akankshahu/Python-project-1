from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.db.session import Base


class TrialPhase(str, enum.Enum):
    PHASE_1 = "Phase 1"
    PHASE_2 = "Phase 2"
    PHASE_3 = "Phase 3"
    PHASE_4 = "Phase 4"


class TrialStatus(str, enum.Enum):
    PLANNED = "Planned"
    ONGOING = "Ongoing"
    COMPLETED = "Completed"
    TERMINATED = "Terminated"


class Drug(Base):
    """Drug/Medication model"""
    __tablename__ = "drugs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    generic_name = Column(String(200))
    manufacturer = Column(String(200))
    approval_date = Column(Date)
    therapeutic_area = Column(String(100))
    molecule_type = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    clinical_trials = relationship("ClinicalTrial", back_populates="drug")
    adverse_events = relationship("AdverseEvent", back_populates="drug")


class ClinicalTrial(Base):
    """Clinical Trial model"""
    __tablename__ = "clinical_trials"

    id = Column(Integer, primary_key=True, index=True)
    trial_id = Column(String(50), unique=True, nullable=False, index=True)
    title = Column(String(500), nullable=False)
    drug_id = Column(Integer, ForeignKey("drugs.id"))
    phase = Column(SQLEnum(TrialPhase))
    status = Column(SQLEnum(TrialStatus))
    start_date = Column(Date)
    end_date = Column(Date)
    patient_count = Column(Integer)
    location = Column(String(200))
    sponsor = Column(String(200))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    drug = relationship("Drug", back_populates="clinical_trials")
    trial_results = relationship("TrialResult", back_populates="trial")


class TrialResult(Base):
    """Clinical Trial Results model"""
    __tablename__ = "trial_results"

    id = Column(Integer, primary_key=True, index=True)
    trial_id = Column(Integer, ForeignKey("clinical_trials.id"))
    endpoint = Column(String(200))
    result_value = Column(Float)
    unit = Column(String(50))
    p_value = Column(Float)
    confidence_interval = Column(String(100))
    notes = Column(String(1000))
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    trial = relationship("ClinicalTrial", back_populates="trial_results")


class AdverseEvent(Base):
    """Adverse Events model"""
    __tablename__ = "adverse_events"

    id = Column(Integer, primary_key=True, index=True)
    drug_id = Column(Integer, ForeignKey("drugs.id"))
    event_type = Column(String(200))
    severity = Column(String(50))
    frequency = Column(Integer)
    description = Column(String(1000))
    reported_date = Column(Date)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    drug = relationship("Drug", back_populates="adverse_events")
