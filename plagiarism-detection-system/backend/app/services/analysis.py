from sqlalchemy.orm import Session
from app.models import models
from app.engines import stylometry, ai_detection, similarity
import json

def analyze_submission(db: Session, submission_id: int):
    submission = db.query(models.Submission).filter(models.Submission.submission_id == submission_id).first()
    if not submission:
        return None
    
    text = submission.extracted_text
    
    # 1. Stylometric Analysis
    stylo_result = stylometry.analyze_stylometry(text)
    
    # Update Student Profile (Simplified: just storing the latest for now, should be aggregated)
    profile = db.query(models.StylometricProfile).filter(models.StylometricProfile.student_id == submission.student_id).first()
    if not profile:
        profile = models.StylometricProfile(
            student_id=submission.student_id,
            avg_sentence_length=stylo_result["avg_sentence_length"],
            type_token_ratio=stylo_result["type_token_ratio"],
            punctuation_distribution=stylo_result["punctuation_distribution"],
            pos_distribution=stylo_result["pos_distribution"],
            fingerprint_vector=stylo_result["fingerprint_vector"]
        )
        db.add(profile)
    else:
        # Update existing profile logic (simplified)
        profile.avg_sentence_length = stylo_result["avg_sentence_length"]
        profile.type_token_ratio = stylo_result["type_token_ratio"]
        profile.fingerprint_vector = stylo_result["fingerprint_vector"]
    
    # Calculate Deviation (Mock logic: euclidean distance from previous vector if exists)
    # For now, we'll just use a placeholder deviation based on randomness or standard deviation
    stylometric_deviation = 0.05 # Low deviation by default
    
    # 2. AI Detection
    ai_score = ai_detection.detect_ai_content(text)
    
    # 3. Semantic Similarity
    # Build corpus from other submissions
    other_submissions = db.query(models.Submission).filter(models.Submission.submission_id != submission_id).all()
    corpus = [s.extracted_text for s in other_submissions]
    similarity_score = similarity.calculate_similarity(text, corpus)
    
    # 4. Risk Scoring
    # Risk = (0.4 * Stylometric) + (0.3 * AI) + (0.3 * Similarity)
    # Note: Stylometric deviation needs normalization. We assume 0-1 for now.
    risk_score = (0.4 * stylometric_deviation) + (0.3 * ai_score) + (0.3 * similarity_score)
    
    risk_level = "Low"
    if risk_score > 0.6:
        risk_level = "High"
    elif risk_score > 0.3:
        risk_level = "Medium"
        
    # Save Report
    detection_result = models.DetectionResult(
        submission_id=submission_id,
        stylometric_deviation_score=stylometric_deviation,
        ai_probability_score=ai_score,
        semantic_similarity_score=similarity_score,
        final_risk_level=risk_level
    )
    db.add(detection_result)
    db.commit()
    
    return detection_result
