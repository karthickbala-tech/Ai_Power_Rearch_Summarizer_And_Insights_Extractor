import json
import bcrypt
from pathlib import Path
from datetime import datetime, timedelta
from jose import jwt, JWTError
from app.core.config import JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRE_MINUTES

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))

# parents[0]=app/auth, parents[1]=app, parents[2]=project root
USERS_FILE = Path(__file__).resolve().parents[2] / "users.json"

def load_users() -> list:
    if not USERS_FILE.exists():
        return []
    with open(USERS_FILE) as f:
        return json.load(f).get("users", [])

def get_user(username: str) -> dict | None:
    for user in load_users():
        if user["username"] == username:
            return user
    return None

def authenticate_user(username: str, password: str) -> dict | None:
    user = get_user(username)
    if not user:
        return None
    if not verify_password(password, user["password"]):
        return None
    return user

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire    = datetime.utcnow() + timedelta(minutes=JWT_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)

def decode_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except JWTError:
        return None