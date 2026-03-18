import numpy as np
from app.utils.pdf_utils import extract_text_with_pages
from app.utils.chunking import chunk_text
from app.utils.embedding import embed_texts
from app.core.faiss_index import index, metadata_store, persist_index

def ingest_pdf(file_path: str, paper_id: str):
    pages      = extract_text_with_pages(file_path)
    chunks     = chunk_text(pages)
    if not chunks:
        return
    texts      = [c["text"] for c in chunks]
    embeddings = embed_texts(texts)
    for i, emb in enumerate(embeddings):
        index.add(np.array([emb]))
        faiss_id = str(index.ntotal - 1)
        metadata_store[faiss_id] = {
            "paper_id": paper_id,
            "text":     chunks[i]["text"],
            "page":     chunks[i]["page"]
        }
    persist_index()