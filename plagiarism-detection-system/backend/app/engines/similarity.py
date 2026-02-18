from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_similarity(target_text: str, corpus: list[str]) -> float:
    """
    Calculates the maximum cosine similarity between the target text and a corpus of texts.
    """
    if not corpus:
        return 0.0
        
    documents = [target_text] + corpus
    
    tfidf_vectorizer = TfidfVectorizer()
    try:
        tfidf_matrix = tfidf_vectorizer.fit_transform(documents)
    except ValueError:
        # Handle empty vocabulary or stop words issues
        return 0.0
        
    # Compute similarity of target (index 0) against all others (index 1 to N)
    cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])
    
    # Return the maximum similarity score found
    if cosine_sim.size > 0:
        return float(cosine_sim.max())
    
    return 0.0
