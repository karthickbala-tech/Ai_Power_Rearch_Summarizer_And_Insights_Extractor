from sentence_transformers import SentenceTransformer
from app.core.config import EMBED_MODEL_NAME

model = SentenceTransformer(EMBED_MODEL_NAME)

def embed_texts(texts: list):
    return model.encode(texts, convert_to_numpy=True)