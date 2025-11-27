"""Script to seed the database with sample data for testing.

Usage:
    # Run locally (requires dependencies installed)
    python seed_data.py
    
    # Or run in Docker container
    docker exec job-matching-backend python -c "$(cat seed_data.py)"
"""
from app.database import init_db, SessionLocal
from app import crud, schemas

def seed_database():
    """Create sample jobs and candidates."""
    # Initialize database
    init_db()
    
    db = SessionLocal()
    
    try:
        print("Creating sample jobs...")
        
        # Sample Jobs
        jobs_data = [
            {
                "title": "Senior Python Developer",
                "description": "We are looking for an experienced Python developer to join our backend team. You'll work on building scalable APIs and microservices.",
                "required_skills": ["Python", "FastAPI", "Docker", "PostgreSQL", "AWS"],
                "min_years_experience": 5
            },
            {
                "title": "Full Stack Engineer",
                "description": "Join our team to build modern web applications using React and Python. Experience with both frontend and backend is required.",
                "required_skills": ["Python", "JavaScript", "React", "FastAPI", "Docker"],
                "min_years_experience": 3
            },
            {
                "title": "DevOps Engineer",
                "description": "Looking for a DevOps engineer to manage our cloud infrastructure and CI/CD pipelines.",
                "required_skills": ["Docker", "Kubernetes", "AWS", "Terraform", "CI/CD"],
                "min_years_experience": 4
            },
            {
                "title": "Junior Software Engineer",
                "description": "Great opportunity for a junior developer to learn and grow. We'll provide mentorship and training.",
                "required_skills": ["Python", "JavaScript"],
                "min_years_experience": 1
            },
            {
                "title": "Machine Learning Engineer",
                "description": "Work on cutting-edge ML models and deploy them to production. Experience with PyTorch or TensorFlow required.",
                "required_skills": ["Python", "PyTorch", "TensorFlow", "Docker", "AWS"],
                "min_years_experience": 3
            },
            {
                "title": "Backend API Developer",
                "description": "Build robust RESTful APIs and microservices. Experience with FastAPI or Flask required.",
                "required_skills": ["Python", "FastAPI", "PostgreSQL", "Docker"],
                "min_years_experience": 2
            },
            {
                "title": "Frontend Developer",
                "description": "Create beautiful and responsive user interfaces. Strong React and CSS skills required.",
                "required_skills": ["JavaScript", "React", "CSS", "HTML"],
                "min_years_experience": 2
            },
            {
                "title": "Cloud Architect",
                "description": "Design and implement cloud infrastructure solutions. Deep AWS knowledge required.",
                "required_skills": ["AWS", "Terraform", "Docker", "Kubernetes", "CI/CD"],
                "min_years_experience": 6
            }
        ]
        
        created_jobs = []
        for job_data in jobs_data:
            job = crud.create_job(db=db, job=schemas.JobCreate(**job_data))
            created_jobs.append(job)
            print(f"  ✓ Created job: {job.title} (ID: {job.id})")
        
        print(f"\nCreated {len(created_jobs)} jobs")
        
        print("\nCreating sample candidates...")
        
        # Sample Candidates
        candidates_data = [
            {
                "name": "Alice Johnson",
                "skills": ["Python", "FastAPI", "Docker", "PostgreSQL", "AWS"],
                "years_experience": 6
            },
            {
                "name": "Bob Smith",
                "skills": ["Python", "JavaScript", "React", "FastAPI"],
                "years_experience": 4
            },
            {
                "name": "Charlie Brown",
                "skills": ["Docker", "Kubernetes", "AWS", "Terraform"],
                "years_experience": 5
            },
            {
                "name": "Diana Prince",
                "skills": ["Python", "JavaScript"],
                "years_experience": 1
            },
            {
                "name": "Eve Williams",
                "skills": ["Python", "PyTorch", "TensorFlow", "Docker"],
                "years_experience": 3
            },
            {
                "name": "Frank Miller",
                "skills": ["Python", "FastAPI", "Docker"],
                "years_experience": 2
            },
            {
                "name": "Grace Lee",
                "skills": ["JavaScript", "React", "CSS", "HTML"],
                "years_experience": 3
            },
            {
                "name": "Henry Davis",
                "skills": ["AWS", "Docker", "Kubernetes"],
                "years_experience": 7
            },
            {
                "name": "Iris Chen",
                "skills": ["Python", "FastAPI", "PostgreSQL", "Docker", "AWS"],
                "years_experience": 4
            },
            {
                "name": "Jack Wilson",
                "skills": ["Python", "Docker"],
                "years_experience": 1
            }
        ]
        
        created_candidates = []
        for candidate_data in candidates_data:
            candidate = crud.create_candidate(db=db, candidate=schemas.CandidateCreate(**candidate_data))
            created_candidates.append(candidate)
            print(f"  ✓ Created candidate: {candidate.name} (ID: {candidate.id})")
        
        print(f"\nCreated {len(created_candidates)} candidates")
        
        print("\n" + "="*60)
        print("Sample Data Created Successfully!")
        print("="*60)
        print("\nYou can now test the application with:")
        print("\nCandidates (try these IDs in the frontend):")
        for i, candidate in enumerate(created_candidates, 1):
            print(f"  {candidate.id}. {candidate.name} - {', '.join(candidate.get_skills_list())} ({candidate.years_experience} years)")
        
        print("\nJobs created:")
        for job in created_jobs:
            print(f"  {job.id}. {job.title} - Requires: {', '.join(job.get_skills_list())} ({job.min_years_experience}+ years)")
        
        print("\n" + "="*60)
        print("Example matches to test:")
        print("="*60)
        print("Candidate 1 (Alice) should match well with Job 1 (Senior Python Developer)")
        print("Candidate 2 (Bob) should match well with Job 2 (Full Stack Engineer)")
        print("Candidate 3 (Charlie) should match well with Job 3 (DevOps Engineer)")
        print("Candidate 4 (Diana) should match well with Job 4 (Junior Software Engineer)")
        print("\nTry accessing: http://localhost:8001")
        print("Enter candidate IDs 1-10 to see their job matches!")
        
    except Exception as e:
        print(f"Error creating sample data: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()

