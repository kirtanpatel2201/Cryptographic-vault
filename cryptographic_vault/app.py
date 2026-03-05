import streamlit as st
import time
import shutil
import os
import json

from core.vault import save_file, list_files, get_file
from core.face_auth import register_face, authenticate_face

# ---------------- DIRECTORIES ----------------
USERS_FILE = "database/users.json"
VAULT_DIR = "storage/vaults"
FACES_DIR = "storage/faces"

# Ensure directories exist
os.makedirs("database", exist_ok=True)
os.makedirs(VAULT_DIR, exist_ok=True)
os.makedirs(FACES_DIR, exist_ok=True)

if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as f:
        json.dump({}, f)

with open(USERS_FILE, "r") as f:
    users = json.load(f)

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Cryptographic Vault", layout="wide")
st.title("🔐 Cryptographic Vault")

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.title("⚙ Tech Stack")
    st.write("• Python")
    st.write("• Streamlit")
    st.write("• OpenCV (Haar Cascade)")
    st.write("• Cryptography (Fernet)")
    st.write("• NumPy")
    st.write("• JSON Database")

    st.divider()
    if st.button("⚠ Reset All Users"):
        # Clear users.json
        with open(USERS_FILE, "w") as f:
            json.dump({}, f)

        # Delete faces
        if os.path.exists(FACES_DIR):
            shutil.rmtree(FACES_DIR)
            os.makedirs(FACES_DIR)

        # Delete vault files
        if os.path.exists(VAULT_DIR):
            shutil.rmtree(VAULT_DIR)
            os.makedirs(VAULT_DIR)

        st.success("All users, faces, and vault files deleted.")

# ---------------- NAVIGATION ----------------
if "page" not in st.session_state:
    st.session_state.page = "login"

col1, col2 = st.columns(2)
with col1:
    if st.button("🔑 Login"):
        st.session_state.page = "login"
with col2:
    if st.button("📝 Register"):
        st.session_state.page = "register"

# ---------------- REGISTER ----------------
if st.session_state.page == "register":
    st.subheader("Create Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Create Account"):
        if username in users:
            st.error("User already exists")
        else:
            users[username] = password
            with open(USERS_FILE, "w") as f:
                json.dump(users, f)

            st.success("Account created successfully")
            st.info("Camera will capture your face automatically")
            time.sleep(2)
            register_face(username)
            st.success("Face registered successfully")

# ---------------- LOGIN ----------------
if st.session_state.page == "login":
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login Securely"):
        if username in users and users[username] == password:
            st.success("Password verified")
            # OLD FACE MESSAGE
            st.warning("⚠ Face detection will start automatically. Please look at the camera.")
            time.sleep(2)
            result = authenticate_face(username)
            if result:
                st.success("Face verified successfully")
                st.session_state.user = username
            else:
                st.error("Face verification failed")
        else:
            st.error("Invalid username or password")

# ---------------- DASHBOARD ----------------
if "user" in st.session_state:
    user = st.session_state.user
    st.sidebar.success(f"Logged in as {user}")

    st.header("📁 Secure Vault")

    uploaded_file = st.file_uploader("Upload File")
    if uploaded_file:
        save_file(user, uploaded_file)
        st.success("File stored securely")

    st.subheader("Stored Files")
    files = list_files(user)

    for file in files:
        original_filename = file.replace(".vault", "")
        col1, col2 = st.columns([4, 1])
        col1.write(original_filename)
        if col2.button("Download", key=file):
            file_data = get_file(user, file)
            st.download_button(
                label="Download File",
                data=file_data,
                file_name=original_filename
            )

    if st.button("Logout"):
        del st.session_state.user
        st.rerun()