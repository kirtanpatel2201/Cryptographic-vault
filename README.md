# 🔐 Cryptographic Vault

A **secure encrypted storage system** built with Python and Streamlit, featuring **layered authentication** with password and **auto face detection**. Designed for multiple file types, your files are encrypted and stored safely, only accessible to verified users.

---

## Features

- **User Accounts**: Register multiple users with unique usernames and passwords.  
- **Two-Factor Authentication**: Password + **automatic face recognition** using OpenCV Haar Cascade.  
- **Encrypted Vault Storage**: Files are encrypted using `Fernet` and stored securely.  
- **Multiple File Types**: Upload PDFs, DOCX, images, PSD, and more.  
- **Download Decrypted Files**: Files are automatically decrypted when downloaded.  
- **Reset Users Button**: Clear all users, face data, and vault files easily.  
- **Tech Stack Sidebar**: Displays the technologies used.  
- Fully runs locally on `localhost` for better security.

---

## Installation

1. Clone this repository:

bash
git clone https://github.com/kirtanpatel2201/Cryptographic-vault.git
cd Cryptographic-vault

2. Install dependencies:

pip install -r requirements.txt

3. Run the app:

streamlit run app.py


##Security Notes

All files are encrypted locally using Fernet symmetric encryption.

Face data is stored locally and used only for authentication.

The app runs entirely on localhost for privacy and security.


##Author

Kirtan Patel – Student / Developer
