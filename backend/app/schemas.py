from typing import List, Optional

from pydantic import BaseModel, EmailStr


class JobBase(BaseModel):
    title: str
    company: str
    location: str
    description: str
    requirements: str


class JobCreate(JobBase):
    pass


class JobRead(JobBase):
    id: int

    class Config:
        from_attributes = True


class ResumeSubmission(BaseModel):
    candidate_name: str
    email: EmailStr
    resume_text: str
    target_job_ids: Optional[List[int]] = None


class ResumeScoreRead(BaseModel):
    id: int
    candidate_name: str
    email: EmailStr
    matched_job_id: int
    score: float

    class Config:
        from_attributes = True


class MatchResult(BaseModel):
    job: JobRead
    score: float





