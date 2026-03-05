import os
import json
import shutil
from cryptography.fernet import Fernet

BASE_DIR = os.getcwd()

DB_DIR = os.path.join(BASE_DIR,"database")
STORAGE_DIR = os.path.join(BASE_DIR,"storage")
FACES_DIR = os.path.join(STORAGE_DIR,"faces")
VAULT_DIR = os.path.join(STORAGE_DIR,"vaults")

USERS_FILE = os.path.join(DB_DIR,"users.json")
KEY_FILE = os.path.join(DB_DIR,"key.key")

def ensure_directories():

    os.makedirs(DB_DIR,exist_ok=True)
    os.makedirs(STORAGE_DIR,exist_ok=True)
    os.makedirs(FACES_DIR,exist_ok=True)
    os.makedirs(VAULT_DIR,exist_ok=True)

    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE,"w") as f:
            json.dump({},f)

    if not os.path.exists(KEY_FILE):

        key = Fernet.generate_key()

        with open(KEY_FILE,"wb") as f:
            f.write(key)

# ---------------- RESET USERS ----------------

def reset_all_users():

    # clear users.json
    with open(USERS_FILE,"w") as f:
        json.dump({},f)

    # delete faces
    if os.path.exists(FACES_DIR):
        shutil.rmtree(FACES_DIR)
        os.makedirs(FACES_DIR)

    # delete vault files
    if os.path.exists(VAULT_DIR):
        shutil.rmtree(VAULT_DIR)
        os.makedirs(VAULT_DIR)