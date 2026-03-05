import os
from core.crypto_utils import encrypt_file, decrypt_file
from utils.helpers import VAULT_DIR

def save_file(user, uploaded_file):

    data = uploaded_file.read()

    encrypted = encrypt_file(data)

    # ✅ Ensure user folder exists
    user_folder = os.path.join(VAULT_DIR, user)
    os.makedirs(user_folder, exist_ok=True)

    path = os.path.join(user_folder, f"{uploaded_file.name}.vault")

    with open(path, "wb") as f:
        f.write(encrypted)


def list_files(user):

    path = os.path.join(VAULT_DIR, user)

    if not os.path.exists(path):
        return []

    return os.listdir(path)


def get_file(user, file):

    path = os.path.join(VAULT_DIR, user, file)

    with open(path, "rb") as f:
        encrypted = f.read()

    return decrypt_file(encrypted)