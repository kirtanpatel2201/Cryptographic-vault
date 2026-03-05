from cryptography.fernet import Fernet
import os
from utils.helpers import KEY_FILE

# Generate key if not exists
if not os.path.exists(KEY_FILE) or os.path.getsize(KEY_FILE) == 0:

    key = Fernet.generate_key()

    with open(KEY_FILE, "wb") as f:
        f.write(key)

# Load key
with open(KEY_FILE, "rb") as f:
    KEY = f.read()

cipher = Fernet(KEY)

def encrypt_file(data):
    return cipher.encrypt(data)

def decrypt_file(data):
    return cipher.decrypt(data)