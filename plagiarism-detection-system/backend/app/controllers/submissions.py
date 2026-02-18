from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models import models
from app.schemas import schemas
from app.services import analysis

router = APIRouter(
    prefix="/submissions",
    tags=["submissions"]
)

@router.post("/analyze", response_model=schemas.DetectionResult)
async def analyze_submission_endpoint(
    student_id: str = Form(...),
    assignment_id: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Read file content
    content = await file.read()
    try:
        text_content = content.decode("utf-8")
    except UnicodeDecodeError:
        # Fallback for non-utf8
        text_content = content.decode("latin-1")
    
    # Create Submission Record
    submission = models.Submission(
        student_id=student_id,
        assignment_id=assignment_id,
        extracted_text=text_content
    )
    db.add(submission)
    db.commit()
    db.refresh(submission)
    
    # Trigger Analysis
    result = analysis.analyze_submission(db, submission.submission_id)
    return result

@router.get("/{submission_id}/report", response_model=schemas.DetectionResult)
def get_report(submission_id: int, db: Session = Depends(get_db)):
    result = db.query(models.DetectionResult).filter(models.DetectionResult.submission_id == submission_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Report not found")
    return result
