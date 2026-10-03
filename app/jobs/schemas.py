from datetime import datetime
from pydantic import BaseModel


class JobCreate(BaseModel):
    report_type: str


class JobRead(BaseModel):
    id: int
    status: str
    result_path: str | None
    created_at: datetime

    class Config:
        from_attributes = True