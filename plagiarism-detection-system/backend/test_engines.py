
import sys
import os

# Fix path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    print("Testing Stylometry Engine...")
    from app.engines import stylometry
    result = stylometry.analyze_stylometry("This is a test sentence. This is another one.")
    print("Stylometry Result:", result)
except Exception as e:
    print(f"FAILED Stylometry: {e}")
    import traceback
    traceback.print_exc()

try:
    print("\nTesting AI Detection Engine...")
    from app.engines import ai_detection
    score = ai_detection.detect_ai_content("This is a test sentence.")
    print("AI Score:", score)
except Exception as e:
    print(f"FAILED AI Detection: {e}")
    traceback.print_exc()

try:
    print("\nTesting Similarity Engine...")
    from app.engines import similarity
    sim = similarity.calculate_similarity("Test", ["Test corpus"])
    print("Similarity Result:", sim)
except Exception as e:
    print(f"FAILED Similarity: {e}")
    traceback.print_exc()
