from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, JSON, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class Student(Base):
    __tablename__ = "students"

    student_id = Column(String, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    department = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    submissions = relationship("Submission", back_populates="student")
    stylometric_profile = relationship("StylometricProfile", back_populates="student", uselist=False)

class Assignment(Base):
    __tablename__ = "assignments"

    assignment_id = Column(String, primary_key=True, index=True)
    course_name = Column(String)
    title = Column(String)
    upload_type = Column(String)  # softcopy / handwritten
    created_at = Column(DateTime, default=datetime.utcnow)

    submissions = relationship("Submission", back_populates="assignment")

class Submission(Base):
    __tablename__ = "submissions"

    submission_id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String, ForeignKey("students.student_id"))
    assignment_id = Column(String, ForeignKey("assignments.assignment_id"))
    extracted_text = Column(Text)
    submission_timestamp = Column(DateTime, default=datetime.utcnow)

    student = relationship("Student", back_populates="submissions")
    assignment = relationship("Assignment", back_populates="submissions")
    detection_result = relationship("DetectionResult", back_populates="submission", uselist=False)

class StylometricProfile(Base):
    __tablename__ = "stylometric_profiles"

    profile_id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String, ForeignKey("students.student_id"))
    avg_sentence_length = Column(Float)
    type_token_ratio = Column(Float)
    punctuation_distribution = Column(JSON)
    pos_distribution = Column(JSON)
    readability_score = Column(Float)
    fingerprint_vector = Column(JSON)
    last_updated = Column(DateTime, default=datetime.utcnow)

    student = relationship("Student", back_populates="stylometric_profile")

class DetectionResult(Base):
    __tablename__ = "detection_results"

    result_id = Column(Integer, primary_key=True, index=True)
    submission_id = Column(Integer, ForeignKey("submissions.submission_id"))
    stylometric_deviation_score = Column(Float)
    ai_probability_score = Column(Float)
    semantic_similarity_score = Column(Float)
    final_risk_level = Column(String)  # Low / Medium / High
    created_at = Column(DateTime, default=datetime.utcnow)

    submission = relationship("Submission", back_populates="detection_result")
