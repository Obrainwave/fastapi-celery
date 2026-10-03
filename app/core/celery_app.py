from celery import Celery
from celery.schedules import crontab
from app.core.config import settings

celery_app = Celery(
    "worker",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["app.jobs.tasks"],
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    task_reject_on_worker_lost=True,
    result_expires=3600,
    task_routes={
        "app.jobs.tasks.generate_report": {"queue": "reports"},
        "app.jobs.tasks.send_notification_email": {"queue": "emails"},
    },
)

celery_app.conf.beat_schedule = {
    "cleanup-expired-jobs-daily": {
        "task": "app.jobs.tasks.cleanup_expired_jobs",
        "schedule": crontab(hour=2, minute=0),
    },
}