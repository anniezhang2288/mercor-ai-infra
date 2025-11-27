"""Unit tests for match algorithm."""
import pytest
from app.models import Job, Candidate
from app.matching import calculate_match_score, get_job_matches


def test_perfect_match():
    """Test perfect match scenario: all skills match, sufficient experience."""
    candidate = Candidate()
    candidate.set_skills_list(["Python", "FastAPI", "Docker"])
    candidate.years_experience = 5
    
    job = Job()
    job.set_skills_list(["Python", "FastAPI", "Docker"])
    job.min_years_experience = 3
    
    score = calculate_match_score(candidate, job)
    
    # Skill match: 3/3 = 1.0
    # Experience match: min(5/3, 1.0) = 1.0
    # Final: round((0.7 * 1.0 + 0.3 * 1.0) * 100) = 100
    assert score == 100


def test_partial_match():
    """Test partial match: some skills match, sufficient experience."""
    candidate = Candidate()
    candidate.set_skills_list(["Python", "Docker"])
    candidate.years_experience = 3
    
    job = Job()
    job.set_skills_list(["Python", "FastAPI", "Docker"])
    job.min_years_experience = 2
    
    score = calculate_match_score(candidate, job)
    
    # Skill match: 2/3 = 0.667
    # Experience match: min(3/2, 1.0) = 1.0
    # Final: round((0.7 * 0.667 + 0.3 * 1.0) * 100) = round(76.69) = 77
    assert score == 77


def test_low_match():
    """Test low match: few skills match, insufficient experience."""
    candidate = Candidate()
    candidate.set_skills_list(["Python"])
    candidate.years_experience = 1
    
    job = Job()
    job.set_skills_list(["Python", "FastAPI", "Docker", "AWS"])
    job.min_years_experience = 5
    
    score = calculate_match_score(candidate, job)
    
    # Skill match: 1/4 = 0.25
    # Experience match: min(1/5, 1.0) = 0.2
    # Final: round((0.7 * 0.25 + 0.3 * 0.2) * 100) = round(23.5) = 24
    assert score == 24


def test_no_skills_match():
    """Test scenario where no skills match."""
    candidate = Candidate()
    candidate.set_skills_list(["Java", "Spring"])
    candidate.years_experience = 5
    
    job = Job()
    job.set_skills_list(["Python", "FastAPI"])
    job.min_years_experience = 2
    
    score = calculate_match_score(candidate, job)
    
    # Skill match: 0/2 = 0.0
    # Experience match: min(5/2, 1.0) = 1.0
    # Final: round((0.7 * 0.0 + 0.3 * 1.0) * 100) = 30
    assert score == 30


def test_zero_experience_required():
    """Test scenario where job requires 0 years experience."""
    candidate = Candidate()
    candidate.set_skills_list(["Python"])
    candidate.years_experience = 0
    
    job = Job()
    job.set_skills_list(["Python"])
    job.min_years_experience = 0
    
    score = calculate_match_score(candidate, job)
    
    # Skill match: 1/1 = 1.0
    # Experience match: 1.0 (since min_years_experience is 0)
    # Final: round((0.7 * 1.0 + 0.3 * 1.0) * 100) = 100
    assert score == 100


def test_get_job_matches_sorting():
    """Test that job matches are sorted by score descending."""
    candidate = Candidate()
    candidate.set_skills_list(["Python", "Docker"])
    candidate.years_experience = 3
    
    job1 = Job()
    job1.id = 1
    job1.title = "Job 1"
    job1.set_skills_list(["Python", "Docker", "FastAPI"])
    job1.min_years_experience = 2
    
    job2 = Job()
    job2.id = 2
    job2.title = "Job 2"
    job2.set_skills_list(["Python", "Docker"])
    job2.min_years_experience = 2
    
    job3 = Job()
    job3.id = 3
    job3.title = "Job 3"
    job3.set_skills_list(["Python"])
    job3.min_years_experience = 2
    
    jobs = [job1, job2, job3]
    matches = get_job_matches(candidate, jobs)
    
    # Job 2 should have highest score (perfect skill match)
    # Job 1 should have second (2/3 skills)
    # Job 3 should have lowest (1/1 but only one skill)
    assert len(matches) == 3
    assert matches[0]["matchScore"] >= matches[1]["matchScore"]
    assert matches[1]["matchScore"] >= matches[2]["matchScore"]

