from sqlalchemy.orm import Session
from app.jobs.repository import JobRepository
from app.jobs.schemas import JobCreate
from app.jobs.tasks import generate_report


class CreateReportJobService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = JobRepository(db)

    def execute(self, payload: JobCreate):
        job = self.repo.create(payload)
        self.db.commit()
        self.db.refresh(job)

        generate_report.delay(job.id)

        return job