import faiss
import os
import json
from app.core.config import EMBED_DIM, INDEX_DIR

index          = faiss.IndexFlatL2(EMBED_DIM)
metadata_store = {}

def persist_index():
    if os.path.exists(INDEX_DIR) and not os.path.isdir(INDEX_DIR):
        os.remove(INDEX_DIR)
    os.makedirs(INDEX_DIR, exist_ok=True)
    faiss.write_index(index, os.path.join(INDEX_DIR, "faiss.index"))
    with open(os.path.join(INDEX_DIR, "metadata.json"), "w") as f:
        json.dump(metadata_store, f)