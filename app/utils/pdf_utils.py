import fitz

def extract_text_with_pages(path: str) -> list:
    doc = fitz.open(path)
    pages = []
    for i, page in enumerate(doc):
        text = page.get_text()
        pages.append({"page": i + 1, "text": text})
    doc.close()
    return pages