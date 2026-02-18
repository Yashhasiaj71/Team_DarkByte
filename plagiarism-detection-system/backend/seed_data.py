from app.core.database import SessionLocal, engine, Base
from app.models import models
from app.engines import stylometry, ai_detection, similarity
import datetime

# Create tables if not exist
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Check if data exists
if db.query(models.Student).first():
    print("Data already exists. Skipping seed.")
    db.close()
    exit()

# 1. Create Students
students = [
    models.Student(student_id="1", full_name="John Doe", email="john@university.edu", department="Computer Science"),
    models.Student(student_id="2", full_name="Alice Smith", email="alice@university.edu", department="English Literature"),
    models.Student(student_id="3", full_name="Bob Jones", email="bob@university.edu", department="History"),
    models.Student(student_id="4", full_name="Emma Wilson", email="emma@university.edu", department="Psychology"),
]

for s in students:
    db.add(s)
db.commit()

# 2. Create Assignments
assignments = [
    models.Assignment(assignment_id="1", course_name="CS101", title="AI Ethics Essay", upload_type="softcopy"),
    models.Assignment(assignment_id="2", course_name="LIT202", title="Shakespeare Analysis", upload_type="softcopy"),
]

for a in assignments:
    db.add(a)
db.commit()

# 3. Create Dummy Submissions & Results
# Re-fetch to get IDs
john = db.query(models.Student).filter_by(email="john@university.edu").first()
alice = db.query(models.Student).filter_by(email="alice@university.edu").first()

cs101_assign = db.query(models.Assignment).filter_by(course_name="CS101").first()

# Submission 1 (John - Authentic)
text1 = "Artificial Intelligence poses significant ethical challenges. One of the primary concerns is bias in algorithms."
sub1 = models.Submission(student_id=john.student_id, assignment_id=cs101_assign.assignment_id, extracted_text=text1)
db.add(sub1)
db.commit()

# Create Result for Sub1
res1 = models.DetectionResult(
    submission_id=sub1.submission_id,
    stylometric_deviation_score=0.1,
    ai_probability_score=0.05,
    semantic_similarity_score=0.0,
    final_risk_level="Low"
)
db.add(res1)

# Submission 2 (Alice - Plagiarized/AI)
text2 = "Artificial Intelligence presents major ethical dilemmas. A key issue is algorithmic bias." # Similar to text1
sub2 = models.Submission(student_id=alice.student_id, assignment_id=cs101_assign.assignment_id, extracted_text=text2)
db.add(sub2)
db.commit()

# Create Result for Sub2
res2 = models.DetectionResult(
    submission_id=sub2.submission_id,
    stylometric_deviation_score=0.8,
    ai_probability_score=0.9,
    semantic_similarity_score=0.85,
    final_risk_level="High"
)
db.add(res2)

db.commit()
db.close()

print("Database seeded successfully!")
