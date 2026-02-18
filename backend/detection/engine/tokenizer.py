"""
Text tokenizer for plagiarism detection.

Normalizes text into a stream of tokens:
- Lowercased
- Punctuation removed
- Common stopwords removed (optional)
"""

import re
import string

# Minimal English stopwords (kept small to preserve structure)
STOPWORDS = frozenset({
    "a", "an", "the", "is", "it", "of", "in", "to", "and", "or",
    "for", "on", "at", "by", "as", "be", "was", "were", "been",
    "are", "has", "had", "have", "do", "does", "did", "but", "not",
    "this", "that", "with", "from", "will", "would", "can", "could",
    "shall", "should", "may", "might", "if", "then", "than", "so",
    "no", "nor", "too", "very", "just",
})


def tokenize(text: str, remove_stopwords: bool = True) -> list[str]:
    """
    Tokenize and normalize a text string.

    Args:
        text: Raw text to tokenize
        remove_stopwords: Whether to filter out common stopwords

    Returns:
        List of normalized tokens
    """
    # Lowercase
    text = text.lower()

    # Remove punctuation (replace with space to avoid merging words)
    text = re.sub(f"[{re.escape(string.punctuation)}]", " ", text)

    # Split into words
    tokens = text.split()

    # Remove stopwords if requested
    if remove_stopwords:
        tokens = [t for t in tokens if t not in STOPWORDS]

    return tokens
