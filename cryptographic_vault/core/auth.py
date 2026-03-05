import json
import hashlib
import os
from core.face_auth import capture_face, verify_face
from utils.helpers import USERS_FILE, VAULT_DIR

def load_users():
    with open(USERS_FILE,"r") as f:
        return json.load(f)

def save_users(data):
    with open(USERS_FILE,"w") as f:
        json.dump(data,f)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username,password):

    users = load_users()

    if username in users:
        return False,"User already exists"

    users[username] = {
        "password": hash_password(password)
    }

    save_users(users)

    os.makedirs(f"{VAULT_DIR}/{username}", exist_ok=True)

    capture_face(username)

    return True,"Account created successfully"

def login_user(username,password):

    users = load_users()

    if username not in users:
        return False,"User not found"

    if users[username]["password"] != hash_password(password):
        return False,"Incorrect password"

    if not verify_face(username):
        return False,"Face authentication failed"

    return True,"Login successful"