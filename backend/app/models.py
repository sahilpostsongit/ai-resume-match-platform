from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, Float, DateTime

from .database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(120), nullable=False)
    company = Column(String(120), nullable=False)
    location = Column(String(120), nullable=False, default="Remote")
    description = Column(Text, nullable=False)
    requirements = Column(Text, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ResumeScore(Base):
    __tablename__ = "resume_scores"

    id = Column(Integer, primary_key=True, index=True)
    candidate_name = Column(String(120), nullable=False)
    email = Column(String(120), nullable=False)
    resume_text = Column(Text, nullable=False)
    matched_job_id = Column(Integer, nullable=False)
    score = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

