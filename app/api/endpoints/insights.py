from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List
from app.services.retrieval_service import retrieve_chunks
from app.services.llm_service import call_llm
from app.auth.auth_bearer import jwt_guard

router = APIRouter()

class InsightsRequest(BaseModel):
    paper_id: str
    questions: List[str]

@router.post("/insights")
def insights(req: InsightsRequest, user=Depends(jwt_guard)):
    results = {}
    for question in req.questions:
        chunks  = retrieve_chunks(question, req.paper_id)
        context = "\n\n".join([f"[Page {c['page']}] {c['text']}" for c in chunks])
        answer  = call_llm(
            "You are a research assistant. Answer based only on the provided context.",
            f"Question: {question}\n\nContext:\n{context}"
        )
        results[question] = answer
    return {"insights": results}