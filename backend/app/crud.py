"""CRUD operations for jobs and candidates."""
from sqlalchemy.orm import Session
from typing import List, Optional
from app import models, schemas


# Job CRUD operations
def create_job(db: Session, job: schemas.JobCreate) -> models.Job:
    """Create a new job."""
    db_job = models.Job(
        title=job.title,
        description=job.description,
        min_years_experience=job.min_years_experience
    )
    db_job.set_skills_list(job.required_skills)
    
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job


def get_job(db: Session, job_id: int) -> Optional[models.Job]:
    """Get a job by ID."""
    return db.query(models.Job).filter(models.Job.id == job_id).first()


def get_all_jobs(db: Session, skip: int = 0, limit: int = 100) -> List[models.Job]:
    """Get all jobs."""
    return db.query(models.Job).offset(skip).limit(limit).all()


def update_job(db: Session, job_id: int, job_update: schemas.JobUpdate) -> Optional[models.Job]:
    """Update a job."""
    db_job = get_job(db, job_id)
    if not db_job:
        return None
    
    if job_update.title is not None:
        db_job.title = job_update.title
    if job_update.description is not None:
        db_job.description = job_update.description
    if job_update.required_skills is not None:
        db_job.set_skills_list(job_update.required_skills)
    if job_update.min_years_experience is not None:
        db_job.min_years_experience = job_update.min_years_experience
    
    db.commit()
    db.refresh(db_job)
    return db_job


def delete_job(db: Session, job_id: int) -> bool:
    """Delete a job."""
    db_job = get_job(db, job_id)
    if not db_job:
        return False
    
    db.delete(db_job)
    db.commit()
    return True


# Candidate CRUD operations
def create_candidate(db: Session, candidate: schemas.CandidateCreate) -> models.Candidate:
    """Create a new candidate."""
    db_candidate = models.Candidate(
        name=candidate.name,
        years_experience=candidate.years_experience
    )
    db_candidate.set_skills_list(candidate.skills)
    
    db.add(db_candidate)
    db.commit()
    db.refresh(db_candidate)
    return db_candidate


def get_candidate(db: Session, candidate_id: int) -> Optional[models.Candidate]:
    """Get a candidate by ID."""
    return db.query(models.Candidate).filter(models.Candidate.id == candidate_id).first()


def update_candidate(
    db: Session, 
    candidate_id: int, 
    candidate_update: schemas.CandidateUpdate
) -> Optional[models.Candidate]:
    """Update a candidate."""
    db_candidate = get_candidate(db, candidate_id)
    if not db_candidate:
        return None
    
    if candidate_update.name is not None:
        db_candidate.name = candidate_update.name
    if candidate_update.skills is not None:
        db_candidate.set_skills_list(candidate_update.skills)
    if candidate_update.years_experience is not None:
        db_candidate.years_experience = candidate_update.years_experience
    
    db.commit()
    db.refresh(db_candidate)
    return db_candidate


def delete_candidate(db: Session, candidate_id: int) -> bool:
    """Delete a candidate."""
    db_candidate = get_candidate(db, candidate_id)
    if not db_candidate:
        return False
    
    db.delete(db_candidate)
    db.commit()
    return True

