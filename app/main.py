from fastapi import FastAPI
from app.api.endpoints import upload, summarize, insights, chat
from app.auth.auth_routes import router as auth_router

app = FastAPI(title="ResearchMind AI")

# Public
app.include_router(auth_router)

# Protected
app.include_router(upload.router)
app.include_router(summarize.router)
app.include_router(insights.router)
app.include_router(chat.router)
