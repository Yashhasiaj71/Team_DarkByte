"""
Comparator — orchestrates the full comparison pipeline for a document pair.

Combines text-level (TF-IDF cosine) and syntactic-level (Winnowing fingerprint)
similarity into a unified result.
"""

from .tokenizer import tokenize
from .winnowing import compute_fingerprints
from .similarity import (
    tfidf_cosine_similarity,
    jaccard_similarity,
    find_matching_fingerprints,
    find_flagged_segments,
)


def compare_documents(
    text_a: str,
    text_b: str,
    k: int = 5,
    window_size: int = 4,
    text_weight: float = 0.4,
    fingerprint_weight: float = 0.6,
) -> dict:
    """
    Run the full plagiarism comparison pipeline on two document texts.

    Args:
        text_a: Raw text of document A
        text_b: Raw text of document B
        k: K-gram size for Winnowing (default: 5)
        window_size: Winnowing window size (default: 4)
        text_weight: Weight for TF-IDF similarity in final score
        fingerprint_weight: Weight for fingerprint similarity in final score

    Returns:
        Dict with similarity scores and detailed match information:
        {
            "similarity_pct": float,
            "text_similarity": float,
            "fingerprint_similarity": float,
            "matched_fingerprints": int,
            "total_fingerprints_a": int,
            "total_fingerprints_b": int,
            "flagged_segments": [...],
        }
    """
    # ── Text-level similarity ────────────────────────
    text_sim = tfidf_cosine_similarity(text_a, text_b)

    # ── Syntactic fingerprinting ─────────────────────
    tokens_a = tokenize(text_a)
    tokens_b = tokenize(text_b)

    fingerprints_a = compute_fingerprints(tokens_a, k=k, window_size=window_size)
    fingerprints_b = compute_fingerprints(tokens_b, k=k, window_size=window_size)

    fp_sim = jaccard_similarity(fingerprints_a, fingerprints_b)

    # ── Matching fingerprints & flagged segments ─────
    matches = find_matching_fingerprints(fingerprints_a, fingerprints_b)
    flagged = find_flagged_segments(matches)

    # ── Combined score ───────────────────────────────
    combined = text_weight * text_sim + fingerprint_weight * fp_sim
    similarity_pct = round(combined * 100, 2)

    return {
        "similarity_pct": similarity_pct,
        "text_similarity": round(text_sim * 100, 2),
        "fingerprint_similarity": round(fp_sim * 100, 2),
        "matched_fingerprints": len(matches),
        "total_fingerprints_a": len(fingerprints_a),
        "total_fingerprints_b": len(fingerprints_b),
        "flagged_segments": flagged,
    }
