from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db import get_db
from app.schemas.schemas import DrugCreate, DrugUpdate, DrugResponse
from app.services.services import DrugService

router = APIRouter(prefix="/drugs", tags=["drugs"])


@router.get("/", response_model=List[DrugResponse])
def get_drugs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get all drugs with pagination
    
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum number of records to return (default: 100)
    """
    drugs = DrugService.get_all_drugs(db, skip=skip, limit=limit)
    return drugs


@router.get("/{drug_id}", response_model=DrugResponse)
def get_drug(drug_id: int, db: Session = Depends(get_db)):
    """
    Get a specific drug by ID
    
    - **drug_id**: The ID of the drug to retrieve
    """
    drug = DrugService.get_drug_by_id(db, drug_id)
    if not drug:
        raise HTTPException(status_code=404, detail="Drug not found")
    return drug


@router.post("/", response_model=DrugResponse, status_code=status.HTTP_201_CREATED)
def create_drug(drug: DrugCreate, db: Session = Depends(get_db)):
    """
    Create a new drug
    
    - **name**: Drug name (required)
    - **generic_name**: Generic name of the drug
    - **manufacturer**: Drug manufacturer
    - **approval_date**: FDA approval date
    - **therapeutic_area**: Therapeutic area (e.g., Oncology, Cardiology)
    - **molecule_type**: Type of molecule (e.g., Small Molecule, Biologic)
    """
    return DrugService.create_drug(db, drug)


@router.put("/{drug_id}", response_model=DrugResponse)
def update_drug(drug_id: int, drug: DrugUpdate, db: Session = Depends(get_db)):
    """
    Update an existing drug
    
    - **drug_id**: The ID of the drug to update
    """
    updated_drug = DrugService.update_drug(db, drug_id, drug)
    if not updated_drug:
        raise HTTPException(status_code=404, detail="Drug not found")
    return updated_drug


@router.delete("/{drug_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_drug(drug_id: int, db: Session = Depends(get_db)):
    """
    Delete a drug
    
    - **drug_id**: The ID of the drug to delete
    """
    success = DrugService.delete_drug(db, drug_id)
    if not success:
        raise HTTPException(status_code=404, detail="Drug not found")
    return None
