from sqlalchemy.orm import Session
from app.jobs.models import Job
from app.jobs.schemas import JobCreate


class JobRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, payload: JobCreate) -> Job:
        job = Job(status="pending", **payload.model_dump())
        self.db.add(job)
        self.db.flush()
        return job

    def get(self, job_id: int) -> Job | None:
        return self.db.get(Job, job_id)

    def update_status(self, job_id: int, status: str, result_path: str | None = None) -> None:
        job = self.db.get(Job, job_id)
        job.status = status
        if result_path is not None:
            job.result_path = result_path