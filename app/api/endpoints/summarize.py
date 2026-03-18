from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.services.retrieval_service import retrieve_chunks
from app.services.llm_service import call_llm
from app.auth.auth_bearer import jwt_guard

router = APIRouter()

class SummarizeRequest(BaseModel):
    paper_id: str
    length: str = "medium"

LENGTH_PROMPTS = {
    "short": (
        "Write ONLY 3 sentences. Strictly 3 sentences, nothing more. "
        "Each sentence must be concise. Cover only the single most important finding."
    ),
    "medium": (
        "Write EXACTLY 2 paragraphs separated by a blank line. "
        "Each paragraph must have exactly 3 to 4 sentences. "
        "Paragraph 1: the research problem and approach. "
        "Paragraph 2: the key results and conclusion. "
        "Total output must be 2 paragraphs only."
    ),
    "long": (
        "Write EXACTLY 5 paragraphs separated by blank lines. "
        "Each paragraph must have 4 to 5 sentences. "
        "Paragraph 1: background. Paragraph 2: problem and goals. "
        "Paragraph 3: methodology. Paragraph 4: results. "
        "Paragraph 5: conclusions and limitations. "
        "Write all 5 full paragraphs with detail."
    ),
}

@router.post("/summarize")
def summarize(req: SummarizeRequest, user=Depends(jwt_guard)):
    chunks = retrieve_chunks("summarize this research paper", req.paper_id)
    if not chunks:
        return {"summary": "No content found. Please re-upload your PDF and try again."}
    context = "\n\n".join([f"[Page {c['page']}] {c['text']}" for c in chunks])
    rule    = LENGTH_PROMPTS.get(req.length, LENGTH_PROMPTS["medium"])
    summary = call_llm(
        f"You are a research paper summarizer. STRICT RULE: {rule}",
        f"IMPORTANT — follow this rule exactly: {rule}\n\nNow summarize this paper:\n\n{context}"
    )
    return {"summary": summary, "length": req.length}