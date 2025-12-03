import hashlib
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..services.matcher import ResumeMatcher, get_matcher


router = APIRouter(prefix="/resumes", tags=["resumes"])


def _jobs_hash(jobs: List[models.Job]) -> str:
    hash_input = "".join(f"{job.id}:{job.updated_at if hasattr(job, 'updated_at') else ''}" for job in jobs)
    if not hash_input:
        hash_input = "empty"
    return hashlib.sha256(hash_input.encode("utf-8")).hexdigest()


@router.post("/match", response_model=list[schemas.MatchResult])
def match_resume(payload: schemas.ResumeSubmission, db: Session = Depends(get_db)):
    jobs_query = db.query(models.Job)
    if payload.target_job_ids:
        jobs_query = jobs_query.filter(models.Job.id.in_(payload.target_job_ids))
    jobs = jobs_query.all()
    if not jobs:
        raise HTTPException(status_code=400, detail="No jobs available to match against.")

    jobs_tuple = tuple(jobs)
    matcher: ResumeMatcher = get_matcher(_jobs_hash(jobs), jobs_tuple)
    results = matcher.score_resume(payload.resume_text)

    if not results:
        raise HTTPException(status_code=500, detail="Matcher failed to compute scores.")

    matches = []
    for job, score in results:
        record = models.ResumeScore(
            candidate_name=payload.candidate_name,
            email=payload.email,
            resume_text=payload.resume_text,
            matched_job_id=job.id,
            score=score,
        )
        db.add(record)
        matches.append({"job": job, "score": score})

    db.commit()
    return matches


@router.get("/scores", response_model=list[schemas.ResumeScoreRead])
def list_scores(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return db.query(models.ResumeScore).offset(skip).limit(limit).all()





