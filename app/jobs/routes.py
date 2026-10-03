from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.jobs.schemas import JobCreate, JobRead
from app.jobs.service import CreateReportJobService

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post("", response_model=JobRead, status_code=201)
def create_job(payload: JobCreate, db: Session = Depends(get_db)):
    service = CreateReportJobService(db)
    job = service.execute(payload)
    return job