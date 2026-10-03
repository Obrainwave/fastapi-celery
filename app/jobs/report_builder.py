import os
from datetime import datetime, timezone
from reportlab.pdfgen import canvas

REPORTS_DIR = "generated_reports"


def build_report_file(job_id: int) -> str:
    os.makedirs(REPORTS_DIR, exist_ok=True)

    file_path = os.path.join(REPORTS_DIR, f"report_{job_id}.pdf")
    timestamp = datetime.now(timezone.utc).isoformat()

    pdf = canvas.Canvas(file_path)
    pdf.drawString(100, 750, f"Report for job {job_id}")
    pdf.drawString(100, 730, f"Generated at {timestamp}")
    pdf.save()

    return file_path