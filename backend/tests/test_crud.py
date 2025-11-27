"""Unit tests for CRUD operations."""
import pytest
from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.database import Base, engine, SessionLocal


@pytest.fixture
def db():
    """Create a test database session."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


def test_create_job(db: Session):
    """Test creating a job."""
    job_data = schemas.JobCreate(
        title="Software Engineer",
        description="Build amazing software",
        required_skills=["Python", "FastAPI"],
        min_years_experience=2
    )
    job = crud.create_job(db=db, job=job_data)
    
    assert job.id is not None
    assert job.title == "Software Engineer"
    assert job.get_skills_list() == ["Python", "FastAPI"]
    assert job.min_years_experience == 2


def test_get_job(db: Session):
    """Test getting a job by ID."""
    job_data = schemas.JobCreate(
        title="Software Engineer",
        description="Build amazing software",
        required_skills=["Python"],
        min_years_experience=2
    )
    created_job = crud.create_job(db=db, job=job_data)
    
    retrieved_job = crud.get_job(db=db, job_id=created_job.id)
    
    assert retrieved_job is not None
    assert retrieved_job.id == created_job.id
    assert retrieved_job.title == "Software Engineer"


def test_get_job_not_found(db: Session):
    """Test getting a non-existent job."""
    job = crud.get_job(db=db, job_id=999)
    assert job is None


def test_get_all_jobs(db: Session):
    """Test getting all jobs."""
    job1 = schemas.JobCreate(
        title="Job 1",
        description="Description 1",
        required_skills=["Python"],
        min_years_experience=1
    )
    job2 = schemas.JobCreate(
        title="Job 2",
        description="Description 2",
        required_skills=["Java"],
        min_years_experience=2
    )
    
    crud.create_job(db=db, job=job1)
    crud.create_job(db=db, job=job2)
    
    jobs = crud.get_all_jobs(db=db)
    assert len(jobs) >= 2


def test_update_job(db: Session):
    """Test updating a job."""
    job_data = schemas.JobCreate(
        title="Software Engineer",
        description="Build amazing software",
        required_skills=["Python"],
        min_years_experience=2
    )
    created_job = crud.create_job(db=db, job=job_data)
    
    update_data = schemas.JobUpdate(
        title="Senior Software Engineer",
        min_years_experience=5
    )
    updated_job = crud.update_job(db=db, job_id=created_job.id, job_update=update_data)
    
    assert updated_job.title == "Senior Software Engineer"
    assert updated_job.min_years_experience == 5
    assert updated_job.description == "Build amazing software"  # Unchanged


def test_delete_job(db: Session):
    """Test deleting a job."""
    job_data = schemas.JobCreate(
        title="Software Engineer",
        description="Build amazing software",
        required_skills=["Python"],
        min_years_experience=2
    )
    created_job = crud.create_job(db=db, job=job_data)
    
    success = crud.delete_job(db=db, job_id=created_job.id)
    assert success is True
    
    deleted_job = crud.get_job(db=db, job_id=created_job.id)
    assert deleted_job is None


def test_create_candidate(db: Session):
    """Test creating a candidate."""
    candidate_data = schemas.CandidateCreate(
        name="John Doe",
        skills=["Python", "FastAPI", "Docker"],
        years_experience=3
    )
    candidate = crud.create_candidate(db=db, candidate=candidate_data)
    
    assert candidate.id is not None
    assert candidate.name == "John Doe"
    assert candidate.get_skills_list() == ["Python", "FastAPI", "Docker"]
    assert candidate.years_experience == 3


def test_get_candidate(db: Session):
    """Test getting a candidate by ID."""
    candidate_data = schemas.CandidateCreate(
        name="John Doe",
        skills=["Python"],
        years_experience=3
    )
    created_candidate = crud.create_candidate(db=db, candidate=candidate_data)
    
    retrieved_candidate = crud.get_candidate(db=db, candidate_id=created_candidate.id)
    
    assert retrieved_candidate is not None
    assert retrieved_candidate.id == created_candidate.id
    assert retrieved_candidate.name == "John Doe"


def test_update_candidate(db: Session):
    """Test updating a candidate."""
    candidate_data = schemas.CandidateCreate(
        name="John Doe",
        skills=["Python"],
        years_experience=3
    )
    created_candidate = crud.create_candidate(db=db, candidate=candidate_data)
    
    update_data = schemas.CandidateUpdate(
        name="Jane Doe",
        years_experience=5
    )
    updated_candidate = crud.update_candidate(
        db=db,
        candidate_id=created_candidate.id,
        candidate_update=update_data
    )
    
    assert updated_candidate.name == "Jane Doe"
    assert updated_candidate.years_experience == 5


def test_delete_candidate(db: Session):
    """Test deleting a candidate."""
    candidate_data = schemas.CandidateCreate(
        name="John Doe",
        skills=["Python"],
        years_experience=3
    )
    created_candidate = crud.create_candidate(db=db, candidate=candidate_data)
    
    success = crud.delete_candidate(db=db, candidate_id=created_candidate.id)
    assert success is True
    
    deleted_candidate = crud.get_candidate(db=db, candidate_id=created_candidate.id)
    assert deleted_candidate is None

