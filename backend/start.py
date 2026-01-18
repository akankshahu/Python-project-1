#!/usr/bin/env python3
"""
Simple database initialization and server startup
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import Base, engine
from app.models.models import Drug, ClinicalTrial, TrialResult, AdverseEvent
from sqlalchemy.orm import Session, sessionmaker
from datetime import date

print("🚀 Initializing DataMAx...")

# Create tables
print("📦 Creating database tables...")
Base.metadata.create_all(bind=engine)
print("✅ Tables created")

# Add sample data
print("📝 Adding sample data...")
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

try:
    # Check if data already exists
    existing_drugs = db.query(Drug).count()
    if existing_drugs > 0:
        print(f"ℹ️  Database already has {existing_drugs} drugs")
    else:
        # Add sample drugs
        drugs = [
            Drug(name="Aspirin", generic_name="Acetylsalicylic acid", manufacturer="Bayer", 
                 therapeutic_area="Cardiology", molecule_type="Small Molecule",
                 approval_date=date(1899, 3, 6)),
            Drug(name="Ibuprofen", generic_name="Ibuprofen", manufacturer="Pfizer",
                 therapeutic_area="Pain Management", molecule_type="Small Molecule",
                 approval_date=date(1969, 1, 1)),
            Drug(name="Metformin", generic_name="Metformin", manufacturer="Merck",
                 therapeutic_area="Endocrinology", molecule_type="Small Molecule",
                 approval_date=date(1994, 12, 29)),
        ]
        
        for drug in drugs:
            db.add(drug)
        db.commit()
        
        # Refresh to get IDs
        for drug in drugs:
            db.refresh(drug)
        
        # Add sample trials
        trials = [
            ClinicalTrial(trial_id="NCT00001", title="Phase 3 Study of Aspirin in CAD",
                         drug_id=drugs[0].id, phase="Phase 3", status="Completed",
                         patient_count=500, location="USA", sponsor="Bayer",
                         start_date=date(2020, 1, 15), end_date=date(2022, 12, 31)),
            ClinicalTrial(trial_id="NCT00002", title="Safety Study of Ibuprofen",
                         drug_id=drugs[1].id, phase="Phase 2", status="Ongoing",
                         patient_count=250, location="EU", sponsor="Pfizer",
                         start_date=date(2021, 6, 1)),
            ClinicalTrial(trial_id="NCT00003", title="Metformin in Type 2 Diabetes",
                         drug_id=drugs[2].id, phase="Phase 3", status="Completed",
                         patient_count=800, location="Global", sponsor="Merck",
                         start_date=date(2018, 11, 5), end_date=date(2021, 8, 20)),
        ]
        
        for trial in trials:
            db.add(trial)
        db.commit()
        
        print(f"✅ Added {len(drugs)} drugs and {len(trials)} clinical trials")
        
except Exception as e:
    print(f"❌ Error: {e}")
    db.rollback()
finally:
    db.close()

print("")
print("=" * 50)
print("✅ DataMAx is ready!")
print("=" * 50)
print("")
print("Starting server...")
print("API Documentation: http://localhost:8000/docs")
print("")

# Start the server
if __name__ == "__main__":
    import uvicorn
    from app.main import app
    uvicorn.run(app, host="0.0.0.0", port=8000)
