"""
Similarity computation module.

Provides:
- TF-IDF cosine similarity (text-level)
- Jaccard similarity of fingerprint sets (syntactic-level)
- Flagged segment detection
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity as sklearn_cosine


def tfidf_cosine_similarity(text_a: str, text_b: str) -> float:
    """
    Compute cosine similarity between two texts using TF-IDF vectors.

    Args:
        text_a: First document text
        text_b: Second document text

    Returns:
        Cosine similarity as a float between 0.0 and 1.0
    """
    if not text_a.strip() or not text_b.strip():
        return 0.0

    vectorizer = TfidfVectorizer()
    try:
        tfidf_matrix = vectorizer.fit_transform([text_a, text_b])
    except ValueError:
        return 0.0

    similarity = sklearn_cosine(tfidf_matrix[0:1], tfidf_matrix[1:2])
    return float(similarity[0][0])


def jaccard_similarity(
    fingerprints_a: list[tuple[int, int]],
    fingerprints_b: list[tuple[int, int]],
) -> float:
    """
    Compute Jaccard similarity of two fingerprint sets (by hash values).

    Args:
        fingerprints_a: Fingerprints of document A as (hash, position) tuples
        fingerprints_b: Fingerprints of document B as (hash, position) tuples

    Returns:
        Jaccard similarity as a float between 0.0 and 1.0
    """
    set_a = {h for h, _ in fingerprints_a}
    set_b = {h for h, _ in fingerprints_b}

    if not set_a and not set_b:
        return 0.0

    intersection = set_a & set_b
    union = set_a | set_b

    return len(intersection) / len(union)


def find_matching_fingerprints(
    fingerprints_a: list[tuple[int, int]],
    fingerprints_b: list[tuple[int, int]],
) -> list[dict]:
    """
    Find matching fingerprint positions between two documents.

    Returns a list of matches indicating which positions in each
    document share the same fingerprint hash.

    Args:
        fingerprints_a: Fingerprints of document A
        fingerprints_b: Fingerprints of document B

    Returns:
        List of dicts with matching position info
    """
    # Build a lookup: hash → list of positions for each doc
    hash_to_pos_a = {}
    for h, pos in fingerprints_a:
        hash_to_pos_a.setdefault(h, []).append(pos)

    hash_to_pos_b = {}
    for h, pos in fingerprints_b:
        hash_to_pos_b.setdefault(h, []).append(pos)

    # Find common hashes
    common_hashes = set(hash_to_pos_a.keys()) & set(hash_to_pos_b.keys())

    matches = []
    for h in common_hashes:
        for pos_a in hash_to_pos_a[h]:
            for pos_b in hash_to_pos_b[h]:
                matches.append({
                    "hash": h,
                    "pos_a": pos_a,
                    "pos_b": pos_b,
                })

    # Sort by position in document A
    matches.sort(key=lambda m: m["pos_a"])
    return matches


def find_flagged_segments(
    matches: list[dict], gap_threshold: int = 3
) -> list[dict]:
    """
    Cluster consecutive matching positions into flagged segments.

    Groups matches that are within `gap_threshold` positions of each
    other into contiguous segments.

    Args:
        matches: List of match dicts from find_matching_fingerprints
        gap_threshold: Maximum gap between positions to merge into one segment

    Returns:
        List of flagged segment dicts
    """
    if not matches:
        return []

    segments = []
    current_segment = {
        "doc_a_start": matches[0]["pos_a"],
        "doc_a_end": matches[0]["pos_a"],
        "doc_b_start": matches[0]["pos_b"],
        "doc_b_end": matches[0]["pos_b"],
        "match_count": 1,
    }

    for match in matches[1:]:
        # If this match is close enough to the current segment, extend it
        if match["pos_a"] - current_segment["doc_a_end"] <= gap_threshold:
            current_segment["doc_a_end"] = match["pos_a"]
            current_segment["doc_b_end"] = max(
                current_segment["doc_b_end"], match["pos_b"]
            )
            current_segment["match_count"] += 1
        else:
            # Start a new segment
            segments.append(current_segment)
            current_segment = {
                "doc_a_start": match["pos_a"],
                "doc_a_end": match["pos_a"],
                "doc_b_start": match["pos_b"],
                "doc_b_end": match["pos_b"],
                "match_count": 1,
            }

    segments.append(current_segment)
    return segments
