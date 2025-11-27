# Job Matching Platform

A lightweight job-matching platform with a FastAPI backend and vanilla JavaScript frontend. The system allows candidates to view job postings and see their match scores based on skills and experience.

## Architecture

### Backend
- **Framework**: FastAPI (Python 3.11)
- **Database**: SQLite (file-based persistence)
- **ORM**: SQLAlchemy
- **API**: RESTful endpoints for jobs, candidates, and matching

### Frontend
- **Technology**: Vanilla HTML/CSS/JavaScript (no frameworks)
- **Location**: `/frontend` directory
- **Pages**: Login page and Jobs list page with navigation
- **Features**: Loading indicators, error handling, responsive design

### Key Features
- CRUD operations for jobs and candidates
- Match score calculation based on skills overlap and experience
- RESTful API with automatic OpenAPI documentation
- Unit tests for match algorithm and CRUD operations
- Docker containerization

## Quick Start

### Prerequisites
- Docker and Docker Compose (optional)
- Python 3.11+ (for local development)
- pip (Python package manager)

### Running with Docker

1. **Build the Docker image:**
   ```bash
   cd backend
   docker build -t job-matching-backend .
   ```

2. **Run the container:**
   ```bash
   docker run -p 8000:8000 job-matching-backend
   ```
   
   **Note:** If port 8000 is already in use, you can use a different port:
   ```bash
   docker run -p 8001:8000 job-matching-backend
   ```
   Then access the app at http://localhost:8001

3. **Access the application:**
   - Frontend: http://localhost:8000
   - API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Running Locally (Development)

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize database:**
   ```bash
   python -c "from app.database import init_db; init_db()"
   ```

5. **Start the server:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

6. **Access the application:**
   - Frontend: http://localhost:8000
   - API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Interactive API docs: http://localhost:8000/redoc

## Frontend Usage

The frontend consists of two pages:

### Login Page (`index.html`)
1. Navigate to http://localhost:8000
2. Enter a candidate ID (must be a positive number)
3. Click "View Matches" to navigate to the jobs list page
4. Form validation ensures a valid candidate ID is entered
5. Error messages displayed for invalid input

### Jobs List Page (`jobs-view.html`)
- Displays all jobs with match scores in a table
- Table columns:
  - **Job Title**: Name of the job position
  - **Required Skills**: List of required skills (displayed as tags)
  - **Min Years Experience**: Minimum years of experience required
  - **Match Score**: Match percentage (0-100)
- Features:
  - Jobs are sorted by match score (highest first)
  - Match scores are color-coded:
    - Green (70-100): High match
    - Orange (40-69): Medium match
    - Red (0-39): Low match
  - "Back to Login" button to return to the login page
  - Loading spinner while fetching data
  - Error messages for invalid candidate IDs or API errors (e.g., "Candidate not found")
  - Responsive design for mobile devices

## API Endpoints

### Jobs

- `POST /jobs` - Create a new job
  ```json
  {
    "title": "Software Engineer",
    "description": "Build amazing software",
    "required_skills": ["Python", "FastAPI", "Docker"],
    "min_years_experience": 2
  }
  ```

- `GET /jobs` - Get all jobs
- `GET /jobs/{jobId}` - Get a specific job
- `PUT /jobs/{jobId}` - Update a job
- `DELETE /jobs/{jobId}` - Delete a job

### Candidates

- `POST /candidates` - Create a new candidate
  ```json
  {
    "name": "John Doe",
    "skills": ["Python", "FastAPI", "Docker"],
    "years_experience": 3
  }
  ```

- `GET /candidates/{candidateId}` - Get a specific candidate
- `PUT /candidates/{candidateId}` - Update a candidate
- `DELETE /candidates/{candidateId}` - Delete a candidate

### Matches

- `GET /candidates/{candidateId}/matches` - Get all jobs with match scores for a candidate
  - Returns array of jobs sorted by match score (descending)
  - Each job includes: `job_id`, `title`, `required_skills`, `min_years_experience`, `match_score`

## Match Algorithm

The match score is calculated using the following formula:

1. **Skill Match Ratio**: `(number of overlapping skills) / (total required skills)`
2. **Experience Match Ratio**: `min(candidate.yearsExperience / job.minYearsExperience, 1.0)`
3. **Final Match Score**: `round((0.7 * skill_match_ratio + 0.3 * experience_match_ratio) * 100)`

**Example:**
- Job requires: `["Python", "FastAPI", "Docker"]` (3 skills), min 2 years
- Candidate has: `["Python", "Docker"]` (2 skills), 3 years experience
- Skill match: 2/3 = 0.667
- Experience match: min(3/2, 1.0) = 1.0
- Final score: round((0.7 * 0.667 + 0.3 * 1.0) * 100) = 77

## Sample Data

To test the application with sample data, you can seed the database:

**Using Docker:**
```bash
docker exec job-matching-backend python seed_data.py
```

Or run the seed script directly in the container:
```bash
docker exec job-matching-backend python -c "$(cat backend/seed_data.py)"
```

This will create:
- **8 sample jobs** with various skill requirements
- **10 sample candidates** with different skill sets and experience levels

**Sample Candidates to Test:**
- **Candidate ID 1** (Alice Johnson): Perfect match for Senior Python Developer (100% score)
  - Skills: Python, FastAPI, Docker, PostgreSQL, AWS | 6 years experience
- **Candidate ID 2** (Bob Smith): Good match for Full Stack Engineer
  - Skills: Python, JavaScript, React, FastAPI | 4 years experience
- **Candidate ID 3** (Charlie Brown): Perfect match for DevOps Engineer
  - Skills: Docker, Kubernetes, AWS, Terraform | 5 years experience
- **Candidate ID 4** (Diana Prince): Good match for Junior Software Engineer
  - Skills: Python, JavaScript | 1 year experience
- **Candidate ID 7** (Grace Lee): Perfect match for Frontend Developer (100% score)
  - Skills: JavaScript, React, CSS, HTML | 3 years experience

**Sample Jobs Created:**
1. Senior Python Developer (5+ years, Python/FastAPI/Docker/AWS)
2. Full Stack Engineer (3+ years, Python/JavaScript/React)
3. DevOps Engineer (4+ years, Docker/Kubernetes/AWS)
4. Junior Software Engineer (1+ year, Python/JavaScript)
5. Machine Learning Engineer (3+ years, Python/PyTorch/TensorFlow)
6. Backend API Developer (2+ years, Python/FastAPI/PostgreSQL)
7. Frontend Developer (2+ years, JavaScript/React/CSS)
8. Cloud Architect (6+ years, AWS/Terraform/Kubernetes)

Try entering candidate IDs 1-10 in the frontend to see their job matches!

## Running Tests

### Option 1: Run Tests in Docker Container (Recommended)

Since the container has all dependencies installed, this is the easiest way:

**Note**: You may need to rebuild the container to include test files:
```bash
docker stop job-matching-backend
docker rm job-matching-backend
docker build -f backend/Dockerfile -t job-matching-backend .
docker run -d -p 8001:8000 --name job-matching-backend job-matching-backend
```

Then run tests:
```bash
# Run all tests
docker exec job-matching-backend pytest

# Run with verbose output (shows each test)
docker exec job-matching-backend pytest -v

# Run specific test file
docker exec job-matching-backend pytest tests/test_matching.py
docker exec job-matching-backend pytest tests/test_crud.py

# Run specific test function
docker exec job-matching-backend pytest tests/test_matching.py::test_perfect_match -v

# Run with output (shows print statements)
docker exec job-matching-backend pytest -v -s
```

### Option 2: Run Tests Locally

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Install dependencies (if not already installed):**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run all tests:**
   ```bash
   pytest
   ```

4. **Run with verbose output:**
   ```bash
   pytest -v
   ```

5. **Run specific test file:**
   ```bash
   pytest tests/test_matching.py
   pytest tests/test_crud.py
   ```

6. **Run specific test function:**
   ```bash
   pytest tests/test_matching.py::test_perfect_match -v
   ```

7. **Run tests with output:**
   ```bash
   pytest -v -s  # -s shows print statements
   ```

### Test Files

- **`tests/test_matching.py`**: Tests for the match algorithm
  - Perfect match scenario
  - Partial match scenario
  - Low match scenario
  - No skills match
  - Zero experience required
  - Sorting verification

- **`tests/test_crud.py`**: Tests for CRUD operations
  - Create, Read, Update, Delete for jobs
  - Create, Read, Update, Delete for candidates
  - Error cases (404, validation)

### Expected Output

When tests pass, you should see:
```
======================== test session starts ========================
collected 15 items

tests/test_crud.py ........                                    [ 53%]
tests/test_matching.py ......                                  [100%]

======================== 15 passed in X.XXs ========================
```

## Project Structure

```
mercor-ai-infra/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI application
│   │   ├── database.py          # Database configuration
│   │   ├── models.py            # SQLAlchemy models
│   │   ├── schemas.py           # Pydantic schemas
│   │   ├── crud.py              # CRUD operations
│   │   ├── matching.py          # Match algorithm
│   │   └── routers/
│   │       ├── jobs.py          # Job endpoints
│   │       ├── candidates.py    # Candidate endpoints
│   │       └── matches.py       # Matching endpoint
│   ├── tests/
│   │   ├── test_matching.py     # Match algorithm tests
│   │   └── test_crud.py         # CRUD operation tests
│   ├── requirements.txt
│   ├── Dockerfile
│   └── pytest.ini
├── frontend/
│   ├── index.html               # Login/input page
│   ├── jobs-view.html          # Jobs list page with matches
│   ├── styles.css              # Styling
│   └── app.js                  # Frontend JavaScript logic
└── README.md
```

## Database

The application uses SQLite for data persistence. The database file (`job_matching.db`) is created automatically in the backend directory when the application starts.

**Tables:**
- `jobs`: Stores job postings
- `candidates`: Stores candidate profiles

## Assumptions & Extensions

### Current Assumptions
- Skills are case-sensitive (e.g., "Python" ≠ "python")
- Match scores are integers from 0-100
- Database persists to file (SQLite)
- Frontend is served statically by the backend

### Extensions for Production (Given More Time)
1. **Authentication & Authorization**
   - JWT-based authentication
   - Role-based access control (admin, recruiter, candidate)

2. **Enhanced Matching**
   - Weighted skills (some skills more important than others)
   - Location-based matching
   - Salary range matching
   - Industry/domain preferences

3. **Database Improvements**
   - Migration to PostgreSQL for production
   - Database migrations with Alembic
   - Connection pooling

4. **API Enhancements**
   - Pagination for large result sets
   - Filtering and sorting options
   - Search functionality
   - Rate limiting

5. **Frontend Improvements**
   - React/Vue.js framework
   - Responsive design
   - Real-time updates
   - Better error handling and user feedback

6. **Testing**
   - Integration tests
   - End-to-end tests
   - Performance testing
   - Load testing

7. **DevOps**
   - CI/CD pipeline
   - Kubernetes deployment
   - Monitoring and logging (Prometheus, Grafana)
   - Health checks and readiness probes

8. **Security**
   - Input validation and sanitization
   - SQL injection prevention (already handled by ORM)
   - CORS configuration for production
   - HTTPS/TLS

## License

This project is part of a coding challenge.
