import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.session import Base, get_db
from app.models.models import Drug, ClinicalTrial

# Create in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db_session():
    """Create a fresh database session for each test"""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db_session):
    """Create a test client with dependency override"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def sample_drug(db_session):
    """Create a sample drug for testing"""
    drug = Drug(
        name="Test Drug",
        generic_name="Test Generic",
        manufacturer="Test Pharma",
        therapeutic_area="Oncology",
        molecule_type="Small Molecule"
    )
    db_session.add(drug)
    db_session.commit()
    db_session.refresh(drug)
    return drug


@pytest.fixture
def sample_trial(db_session, sample_drug):
    """Create a sample clinical trial for testing"""
    trial = ClinicalTrial(
        trial_id="NCT99999",
        title="Test Clinical Trial",
        drug_id=sample_drug.id,
        phase="Phase 3",
        status="Ongoing",
        patient_count=100,
        location="USA",
        sponsor="Test Sponsor"
    )
    db_session.add(trial)
    db_session.commit()
    db_session.refresh(trial)
    return trial
