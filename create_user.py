"""
Run this to add users: python create_user.py
"""
import json
import bcrypt
from pathlib import Path

USERS_FILE = Path(__file__).parent / "users.json"

def create_user(username: str, password: str, full_name: str):
    data = json.load(open(USERS_FILE)) if USERS_FILE.exists() else {"users": []}

    for user in data["users"]:
        if user["username"] == username:
            print(f"❌ User '{username}' already exists.")
            return

    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    data["users"].append({
        "username":  username,
        "password":  hashed,
        "full_name": full_name
    })

    with open(USERS_FILE, "w") as f:
        json.dump(data, f, indent=4)

    print(f"✅ User '{username}' created!")

if __name__ == "__main__":
    print("=== ResearchMind AI — Create User ===")
    username  = input("Username  : ").strip()
    full_name = input("Full Name : ").strip()
    password  = input("Password  : ").strip()
    if username and password:
        create_user(username, password, full_name)
    else:
        print("❌ Username and password cannot be empty.")