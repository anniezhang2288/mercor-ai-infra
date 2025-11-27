"""Match algorithm implementation."""
from typing import List
from app.models import Job, Candidate


def calculate_match_score(candidate: Candidate, job: Job) -> int:
    """
    Calculate match score between a candidate and a job.
    
    Formula:
    - Skill match ratio = (overlapping skills) / (total required skills)
    - Experience match ratio = min(candidate.yearsExperience / job.minYearsExperience, 1.0)
    - Final matchScore = round((0.7 * skill_match_ratio + 0.3 * experience_match_ratio) * 100)
    
    Args:
        candidate: Candidate object
        job: Job object
        
    Returns:
        Match score from 0 to 100
    """
    candidate_skills = set(candidate.get_skills_list())
    job_skills = set(job.get_skills_list())
    
    # Calculate skill match ratio
    if not job_skills:
        skill_match_ratio = 0.0
    else:
        overlapping_skills = candidate_skills.intersection(job_skills)
        skill_match_ratio = len(overlapping_skills) / len(job_skills)
    
    # Calculate experience match ratio
    if job.min_years_experience == 0:
        experience_match_ratio = 1.0
    else:
        experience_match_ratio = min(
            candidate.years_experience / job.min_years_experience,
            1.0
        )
    
    # Calculate final match score
    match_score = round(
        (0.7 * skill_match_ratio + 0.3 * experience_match_ratio) * 100
    )
    
    return match_score


def get_job_matches(candidate: Candidate, jobs: List[Job]) -> List[dict]:
    """
    Get all jobs with match scores for a candidate, sorted by score descending.
    
    Args:
        candidate: Candidate object
        jobs: List of all job objects
        
    Returns:
        List of dictionaries with job info and match score, sorted by score
    """
    matches = []
    
    for job in jobs:
        match_score = calculate_match_score(candidate, job)
        matches.append({
            "jobId": job.id,
            "title": job.title,
            "requiredSkills": job.get_skills_list(),
            "minYearsExperience": job.min_years_experience,
            "matchScore": match_score
        })
    
    # Sort by match score descending
    matches.sort(key=lambda x: x["matchScore"], reverse=True)
    
    return matches

