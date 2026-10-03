from fastapi import FastAPI
from app.jobs.routes import router as jobs_router

app = FastAPI(title="Report Service")

app.include_router(jobs_router)