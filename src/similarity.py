from sklearn.metrics.pairwise import cosine_similarity
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
        candidate_embeddings = [c[2] for c in candidates]
        
        # Reshape target for sklearn (1, n_features)
        target_reshaped = target_embedding.reshape(1, -1)
        
        # Calculate similarities
        # cosine_similarity returns a matrix, we want the first row
        similarities = cosine_similarity(target_reshaped, candidate_embeddings)[0]
        
        # Find index of max similarity
        best_index = np.argmax(similarities)
        best_match = candidates[best_index]
        
        logger.info(f"Best match: '{best_match[0]}' with score {similarities[best_index]:.4f}")
        return best_match[0], best_match[1]

    except Exception as e:
        logger.error(f"Error calculating similarity: {e}")
        return None, None
