"""Pydantic schemas for request/response validation."""
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional


# Job Schemas
class JobBase(BaseModel):
    """Base job schema."""
    title: str
    description: str
    required_skills: List[str] = Field(..., description="List of required skills")
    min_years_experience: int = Field(..., ge=0, description="Minimum years of experience")


class JobCreate(JobBase):
    """Schema for creating a job."""
    pass


class JobUpdate(BaseModel):
    """Schema for updating a job."""
    title: Optional[str] = None
    description: Optional[str] = None
    required_skills: Optional[List[str]] = None
    min_years_experience: Optional[int] = Field(None, ge=0)


class JobResponse(JobBase):
    """Schema for job response."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int


# Candidate Schemas
class CandidateBase(BaseModel):
    """Base candidate schema."""
    name: str
    skills: List[str] = Field(..., description="List of candidate skills")
    years_experience: int = Field(..., ge=0, description="Years of experience")


class CandidateCreate(CandidateBase):
    """Schema for creating a candidate."""
    pass


class CandidateUpdate(BaseModel):
    """Schema for updating a candidate."""
    name: Optional[str] = None
    skills: Optional[List[str]] = None
    years_experience: Optional[int] = Field(None, ge=0)


class CandidateResponse(CandidateBase):
    """Schema for candidate response."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int


# Match Schema
class JobMatch(BaseModel):
    """Schema for job match response."""
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,  # Allow both alias and field name
        json_schema_extra={
            "example": {
                "jobId": 1,
                "title": "Software Engineer",
                "requiredSkills": ["Python", "FastAPI"],
                "minYearsExperience": 2,
                "matchScore": 85
            }
        }
    )
    
    jobId: int
    title: str
    requiredSkills: List[str]
    minYearsExperience: int
    matchScore: int = Field(..., ge=0, le=100, description="Match score from 0 to 100")

