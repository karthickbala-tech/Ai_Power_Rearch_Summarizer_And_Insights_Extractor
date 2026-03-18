import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path)

EMBED_MODEL_NAME   = "all-mpnet-base-v2"
EMBED_DIM          = 768
TOP_K              = 5
DATA_DIR           = "data"
INDEX_DIR          = "index"
GROQ_API_KEY       = os.getenv("GROQ_API_KEY")
GROQ_MODEL         = "llama-3.3-70b-versatile"
JWT_SECRET         = os.getenv("JWT_SECRET", "your_super_secret_key_change_this")
JWT_ALGORITHM      = "HS256"
JWT_EXPIRE_MINUTES = 60 * 8

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY not found.\n"
        f"   Expected .env at: {env_path}\n"
        "   Make sure the file exists and contains: GROQ_API_KEY=your_key_here"
    )