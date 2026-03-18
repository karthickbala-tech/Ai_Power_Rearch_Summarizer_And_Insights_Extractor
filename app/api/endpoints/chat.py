from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional
from app.services.chat_service import add_message, get_history
from app.services.retrieval_service import retrieve_chunks
from app.services.llm_service import call_llm_with_history
from app.auth.auth_bearer import jwt_guard

router = APIRouter()

class ChatRequest(BaseModel):
    session_id: str
    message:    str
    paper_id:   Optional[str] = None

@router.post("/chat")
def chat(req: ChatRequest, user=Depends(jwt_guard)):
    pdf_context = ""
    if req.paper_id:
        chunks = retrieve_chunks(req.message, req.paper_id)
        if chunks:
            pdf_context = "\n\n".join([f"[Page {c['page']}] {c['text']}" for c in chunks])
    add_message(req.session_id, "user", req.message)
    history  = get_history(req.session_id)
    response = call_llm_with_history(history, pdf_context=pdf_context)
    add_message(req.session_id, "assistant", response)
    return {"response": response, "history": get_history(req.session_id)}