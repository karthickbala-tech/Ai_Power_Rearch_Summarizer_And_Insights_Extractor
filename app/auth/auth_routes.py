import json
import bcrypt
from pathlib import Path
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.auth.auth_handler import authenticate_user, create_access_token

router = APIRouter()

USERS_FILE = Path(__file__).resolve().parents[2] / "users.json"

class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username:         str
    full_name:        str
    password:         str
    confirm_password: str

@router.post("/login")
def login(req: LoginRequest):
    user = authenticate_user(req.username, req.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password.")
    token = create_access_token({"sub": user["username"], "name": user.get("full_name", "")})
    return {
        "access_token": token,
        "token_type":   "bearer",
        "username":     user["username"],
        "full_name":    user.get("full_name", "")
    }

@router.post("/register")
def register(req: RegisterRequest):
    if req.password != req.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match.")
    if len(req.password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters.")
    if len(req.username) < 3:
        raise HTTPException(status_code=400, detail="Username must be at least 3 characters.")

    data = json.load(open(USERS_FILE)) if USERS_FILE.exists() else {"users": []}

    for user in data["users"]:
        if user["username"].lower() == req.username.lower():
            raise HTTPException(status_code=409, detail="Username already taken.")

    hashed = bcrypt.hashpw(req.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    data["users"].append({
        "username":  req.username,
        "password":  hashed,
        "full_name": req.full_name
    })

    with open(USERS_FILE, "w") as f:
        json.dump(data, f, indent=4)

    return {"message": f"Account created successfully! Welcome, {req.full_name}."}