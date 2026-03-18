chat_history: dict = {}

def add_message(session_id: str, role: str, content: str):
    if session_id not in chat_history:
        chat_history[session_id] = []
    chat_history[session_id].append({"role": role, "content": content})

def get_history(session_id: str) -> list:
    return chat_history.get(session_id, [])

def clear_history(session_id: str):
    if session_id in chat_history:
        del chat_history[session_id]