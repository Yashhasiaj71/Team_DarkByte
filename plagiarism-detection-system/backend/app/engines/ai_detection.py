import random
import hashlib

def detect_ai_content(text: str) -> float:
    """
    Mock implementation of AI detection.
    Returns a probability score between 0.0 and 1.0.
    """
    # Deterministic mock score based on text hash
    # This ensures the same text always gets the same score for testing
    text_hash = hashlib.md5(text.encode()).hexdigest()
    hash_int = int(text_hash, 16)
    
    # Generate a score between 0 and 100
    score_percent = hash_int % 100
    
    # Normalize to 0-1
    return score_percent / 100.0

def calculate_burstiness(text: str) -> float:
    # Placeholder for burstiness calculation
    return 0.5

def calculate_perplexity(text: str) -> float:
    # Placeholder for perplexity calculation
    return 0.5
