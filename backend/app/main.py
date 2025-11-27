"""FastAPI application entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.database import init_db
from app.routers import jobs, candidates, matches
import os

# Initialize FastAPI app
app = FastAPI(
    title="Job Matching Platform API",
    description="RESTful API for job matching platform",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
def startup_event():
    """Initialize database tables on application startup."""
    init_db()


# Include routers
app.include_router(jobs.router)
app.include_router(candidates.router)
app.include_router(matches.router)

# Serve static files (frontend) if directory exists
# Try multiple possible paths for frontend
frontend_paths = [
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "frontend"),  # Relative from backend/app/
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend"),  # In same directory as backend/
    "/app/frontend",  # Docker container path
    "./frontend",  # Current directory
]

frontend_path = None
for path in frontend_paths:
    if os.path.exists(path):
        frontend_path = path
        break

if frontend_path:
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="static")


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

