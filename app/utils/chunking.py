def chunk_text(pages: list, max_tokens: int = 500, overlap: int = 50) -> list:
    chunks = []
    for page_data in pages:
        text    = page_data["text"]
        page_num = page_data["page"]
        if not text.strip():
            continue
        start = 0
        while start < len(text):
            end   = start + max_tokens
            chunk = text[start:end]
            if chunk.strip():
                chunks.append({"text": chunk, "page": page_num})
            start = end - overlap
            if start >= len(text):
                break
    return chunks