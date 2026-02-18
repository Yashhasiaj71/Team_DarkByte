"""
Winnowing Algorithm for Syntactic Fingerprinting.

Implements the Winnowing algorithm (Schleimer, Wilkerson, Aiken, 2003)
used in tools like MOSS for plagiarism detection.

The algorithm:
1. Generate k-grams (contiguous subsequences of k tokens)
2. Hash each k-gram using a rolling hash
3. Apply a sliding window of size w over the hash sequence
4. From each window, select the minimum hash (rightmost if tie)
5. The selected hashes form the document's "fingerprint"
"""


def _rolling_hash(text: str, base: int = 31, mod: int = (1 << 61) - 1) -> int:
    """Compute a polynomial rolling hash for a string."""
    h = 0
    for ch in text:
        h = (h * base + ord(ch)) % mod
    return h


def generate_kgrams(tokens: list[str], k: int = 5) -> list[str]:
    """
    Generate k-grams from a list of tokens.

    A k-gram is a contiguous subsequence of k tokens joined by spaces.

    Args:
        tokens: List of normalized tokens
        k: Size of each k-gram (default: 5)

    Returns:
        List of k-gram strings
    """
    if len(tokens) < k:
        # If fewer tokens than k, return the whole thing as one gram
        return [" ".join(tokens)] if tokens else []

    return [" ".join(tokens[i : i + k]) for i in range(len(tokens) - k + 1)]


def hash_kgrams(kgrams: list[str]) -> list[tuple[int, int]]:
    """
    Hash each k-gram and return (hash_value, position) pairs.

    Args:
        kgrams: List of k-gram strings

    Returns:
        List of (hash, position) tuples
    """
    return [(_rolling_hash(kg), i) for i, kg in enumerate(kgrams)]


def winnow(hashes: list[tuple[int, int]], window_size: int = 4) -> list[tuple[int, int]]:
    """
    Apply the Winnowing algorithm to select fingerprints.

    For each window of `window_size` consecutive hashes, select the minimum.
    If there's a tie, select the rightmost occurrence.

    Args:
        hashes: List of (hash_value, position) tuples
        window_size: Size of the sliding window (default: 4)

    Returns:
        List of selected (hash, position) fingerprints (deduplicated)
    """
    if not hashes:
        return []
    if len(hashes) <= window_size:
        # Select the minimum from the entire sequence
        min_h = min(hashes, key=lambda x: x[0])
        return [min_h]

    fingerprints = []
    prev_selected = None

    for i in range(len(hashes) - window_size + 1):
        window = hashes[i : i + window_size]

        # Find the minimum hash in the window (rightmost if tie)
        min_hash = None
        for h in window:
            if min_hash is None or h[0] < min_hash[0] or (
                h[0] == min_hash[0] and h[1] >= min_hash[1]
            ):
                min_hash = h

        # Only add if it's a new selection (avoid duplicates)
        if min_hash != prev_selected:
            fingerprints.append(min_hash)
            prev_selected = min_hash

    return fingerprints


def compute_fingerprints(
    tokens: list[str], k: int = 5, window_size: int = 4
) -> list[tuple[int, int]]:
    """
    Full pipeline: tokens → k-grams → hashes → winnowed fingerprints.

    Args:
        tokens: Normalized token list
        k: K-gram size (default: 5)
        window_size: Winnowing window size (default: 4)

    Returns:
        List of (hash, position) fingerprints
    """
    kgrams = generate_kgrams(tokens, k)
    hashes = hash_kgrams(kgrams)
    return winnow(hashes, window_size)
