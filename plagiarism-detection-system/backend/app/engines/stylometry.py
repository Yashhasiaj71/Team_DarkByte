import spacy
import numpy as np
from collections import Counter
import string

# Load English tokenizer, tagger, parser and NER

# Load English tokenizer, tagger, parser and NER
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("ERROR: spacy model 'en_core_web_sm' not found.")
    print("Please run: python -m spacy download en_core_web_sm")
    raise

def analyze_stylometry(text: str) -> dict:
    doc = nlp(text)
    
    # 1. Average Sentence Length
    sentences = list(doc.sents)
    num_sentences = len(sentences)
    num_words = len([token for token in doc if not token.is_punct])
    
    avg_sentence_length = num_words / num_sentences if num_sentences > 0 else 0
    
    # 2. Type-Token Ratio (Vocabulary Richness)
    words = [token.text.lower() for token in doc if not token.is_punct]
    unique_words = set(words)
    type_token_ratio = len(unique_words) / len(words) if len(words) > 0 else 0
    
    # 3. Punctuation Distribution
    punct_counts = Counter([token.text for token in doc if token.is_punct])
    total_puncts = sum(punct_counts.values())
    punct_dist = {k: v / total_puncts for k, v in punct_counts.items()} if total_puncts > 0 else {}
    
    # 4. POS Distribution
    pos_counts = Counter([token.pos_ for token in doc])
    total_pos = sum(pos_counts.values())
    pos_dist = {k: v / total_pos for k, v in pos_counts.items()} if total_pos > 0 else {}
    
    # 5. Fingerprint Vector (Simplified for prototype)
    # Vector = [avg_sent_len, ttr, comman_freq, period_freq]
    fingerprint = [
        avg_sentence_length,
        type_token_ratio,
        pos_dist.get("NOUN", 0),
        pos_dist.get("VERB", 0),
        pos_dist.get("ADJ", 0)
    ]
    
    return {
        "avg_sentence_length": avg_sentence_length,
        "type_token_ratio": type_token_ratio,
        "punctuation_distribution": punct_dist,
        "pos_distribution": pos_dist,
        "fingerprint_vector": fingerprint
    }
