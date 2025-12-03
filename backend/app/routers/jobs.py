from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db


router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("/", response_model=list[schemas.JobRead])
def list_jobs(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return db.query(models.Job).offset(skip).limit(limit).all()


@router.post("/", response_model=schemas.JobRead, status_code=201)
def create_job(job: schemas.JobCreate, db: Session = Depends(get_db)):
    job_model = models.Job(**job.model_dump())
    db.add(job_model)
    db.commit()
    db.refresh(job_model)
    return job_model


@router.get("/{job_id}", response_model=schemas.JobRead)
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job





