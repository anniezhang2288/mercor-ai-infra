"""SQLAlchemy database models."""
from sqlalchemy import Column, Integer, String, Text
from app.database import Base
import json


class Job(Base):
    """Job model."""
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    required_skills = Column(Text, nullable=False)  # Stored as JSON string
    min_years_experience = Column(Integer, nullable=False)

    def get_skills_list(self):
        """Convert skills JSON string to list."""
        return json.loads(self.required_skills) if self.required_skills else []

    def set_skills_list(self, skills):
        """Convert skills list to JSON string."""
        self.required_skills = json.dumps(skills) if skills else "[]"


class Candidate(Base):
    """Candidate model."""
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    skills = Column(Text, nullable=False)  # Stored as JSON string
    years_experience = Column(Integer, nullable=False)

    def get_skills_list(self):
        """Convert skills JSON string to list."""
        return json.loads(self.skills) if self.skills else []

    def set_skills_list(self, skills):
        """Convert skills list to JSON string."""
        self.skills = json.dumps(skills) if skills else "[]"

