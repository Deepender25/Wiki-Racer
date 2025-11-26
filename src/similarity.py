# from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from src.logger_config import setup_logger

logger = setup_logger("Similarity")

def find_closest(target_embedding, candidates):
    """
    Finds the candidate with the highest cosine similarity to the target embedding.
    
    Args:
        target_embedding: The embedding of the target/end page.
        candidates: A list of tuples (title, url, embedding).
        
    Returns:
        The (title, url) of the best match.
    """
    if not candidates:
        return None, None

    try:
        # Extract embeddings from candidates
        # Stack them into a numpy array for vectorized operation
        candidate_embeddings = np.array([c[2] for c in candidates])
        
        # Target embedding is already a 1D array (shape: (384,))
        # Candidate embeddings is 2D array (shape: (N, 384))
        
        # Calculate dot products (Vectorized Inner Product)
        # Since embeddings are normalized, Dot Product = Cosine Similarity
        # This is much faster than sklearn's generic cosine_similarity for this specific case
        similarities = np.dot(candidate_embeddings, target_embedding)
        
        # Find index of max similarity
        best_index = np.argmax(similarities)
        best_match = candidates[best_index]
        
        logger.info(f"Best match: '{best_match[0]}' with score {similarities[best_index]:.4f}")
        return best_match[0], best_match[1]

    except Exception as e:
        logger.error(f"Error calculating similarity: {e}")
        return None, None
