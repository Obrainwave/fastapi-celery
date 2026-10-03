from celery.exceptions import SoftTimeLimitExceeded
from app.core.celery_app import celery_app
from app.core.database import SessionLocal
from app.jobs.repository import JobRepository
from app.jobs.report_builder import build_report_file


@celery_app.task(
    bind=True,
    max_retries=5,
    soft_time_limit=50,
    time_limit=60,
)
def generate_report(self, job_id: int):
    db = SessionLocal()
    repo = JobRepository(db)

    try:
        job = repo.get(job_id)

        if job.status == "completed":
            return

        repo.update_status(job_id, "processing")
        db.commit()

        result_path = build_report_file(job_id)

        repo.update_status(job_id, "completed", result_path=result_path)
        db.commit()

    except SoftTimeLimitExceeded:
        repo.update_status(job_id, "failed")
        db.commit()

    except Exception as exc:
        db.rollback()
        countdown = 2 ** self.request.retries * 10
        raise self.retry(exc=exc, countdown=countdown)

    finally:
        db.close()