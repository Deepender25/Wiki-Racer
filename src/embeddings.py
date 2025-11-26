from sentence_transformers import SentenceTransformer
from src.logger_config import setup_logger

logger = setup_logger("Embeddings")

# Global variable to hold the model instance
_model = None

def load_model():
    global _model
    if _model is None:
        logger.info("Loading sentence-transformers model...")
        try:
            _model = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("Model loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise e
    return _model

def get_embedding(text):
    """
    Returns the vector embedding for the given text.
    """
    model = load_model()
    try:
        embedding = model.encode(text)
        return embedding
    except Exception as e:
        logger.error(f"Error generating embedding for '{text}': {e}")
        return None

def get_embeddings(texts):
    """
    Returns a list of embeddings for a list of texts.
    """
    model = load_model()
    try:
        embeddings = model.encode(texts)
        return embeddings
    except Exception as e:
        logger.error(f"Error generating embeddings for list of size {len(texts)}: {e}")
        return []
