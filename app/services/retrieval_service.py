import numpy as np
from app.utils.embedding import embed_texts
from app.core.faiss_index import index, metadata_store
from app.core.config import TOP_K

def retrieve_chunks(query: str, paper_id: str) -> list:
    if index.ntotal == 0:
        return []
    q_emb    = embed_texts([query])[0]
    D, I     = index.search(np.array([q_emb]), TOP_K)
    results  = []
    for vid in I[0]:
        if vid == -1:
            continue
        meta = metadata_store.get(str(vid))
        if meta and meta["paper_id"] == paper_id:
            results.append(meta)
    return results