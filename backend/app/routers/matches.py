"""Matching endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import crud, matching, schemas
from app.database import get_db

router = APIRouter(prefix="/candidates", tags=["matches"])


@router.get("/{candidate_id}/matches", response_model=List[schemas.JobMatch], response_model_by_alias=False)
def get_candidate_matches(candidate_id: int, db: Session = Depends(get_db)):
    """
    Get all jobs with match scores for a specific candidate.
    Results are sorted by match score descending.
    """
    # Get candidate
    candidate = crud.get_candidate(db=db, candidate_id=candidate_id)
    if candidate is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Candidate with id {candidate_id} not found"
        )
    
    # Get all jobs
    jobs = crud.get_all_jobs(db=db)
    
    # Calculate matches (returns list of dicts)
    matches_dicts = matching.get_job_matches(candidate, jobs)
    
    # Convert dicts to Pydantic models for proper serialization
    matches = [schemas.JobMatch(**match_dict) for match_dict in matches_dicts]
    
    return matches

