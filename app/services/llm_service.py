from groq import Groq
from app.core.config import GROQ_API_KEY, GROQ_MODEL

client = Groq(api_key=GROQ_API_KEY)

def call_llm(system_prompt: str, user_prompt: str) -> str:
    chat = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_prompt},
        ]
    )
    return chat.choices[0].message.content

def call_llm_with_history(history: list, pdf_context: str = "") -> str:
    if pdf_context:
        system = (
            "You are a helpful research assistant. "
            "The user has uploaded a research paper. "
            "Use the following excerpts to answer questions accurately. "
            "Always refer to the paper content when relevant. "
            "Remember everything discussed in this conversation.\n\n"
            "--- PAPER EXCERPTS ---\n"
            f"{pdf_context}\n"
            "--- END OF EXCERPTS ---"
        )
    else:
        system = (
            "You are a helpful research assistant. "
            "Answer based on the conversation history. "
            "Remember everything discussed so far."
        )
    messages = [{"role": "system", "content": system}] + history
    chat = client.chat.completions.create(model=GROQ_MODEL, messages=messages)
    return chat.choices[0].message.content