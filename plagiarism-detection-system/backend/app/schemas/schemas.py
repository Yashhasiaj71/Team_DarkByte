from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

# Student Schemas
class StudentBase(BaseModel):
    full_name: str
    email: str
    department: str

class StudentCreate(StudentBase):
    pass

class Student(StudentBase):
    student_id: str
    created_at: datetime

    class Config:
        orm_mode = True

# Assignment Schemas
class AssignmentBase(BaseModel):
    course_name: str
    title: str
    upload_type: str

class AssignmentCreate(AssignmentBase):
    pass

class Assignment(AssignmentBase):
    assignment_id: str
    created_at: datetime

    class Config:
        orm_mode = True

# Submission Schemas
class SubmissionBase(BaseModel):
    student_id: str
    assignment_id: str

class SubmissionCreate(SubmissionBase):
    extracted_text: str

class Submission(SubmissionBase):
    submission_id: int
    submission_timestamp: datetime

    class Config:
        orm_mode = True

# Detection Result Schemas
class DetectionResultBase(BaseModel):
    stylometric_deviation_score: float
    ai_probability_score: float
    semantic_similarity_score: float
    final_risk_level: str

class DetectionResult(DetectionResultBase):
    result_id: int
    created_at: datetime

    class Config:
        orm_mode = True
