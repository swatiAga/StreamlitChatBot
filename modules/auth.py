import streamlit as st
import os
import json
from modules.config import embed_tool
from modules.bot_purpose import bot_purpose


def load_users():
    """Loads user data from a JSON file."""
    if os.path.exists("users.json"):
        with open("users.json", "r") as file:
            return json.load(file)
    return {}

def save_users(users):
    """Saves user data to a JSON file."""
    with open("users.json", "w") as file:
        json.dump(users, file, indent=4)

def login_signup():
    """
    Displays a login/signup interface using Streamlit and handles user authentication.
    The function provides input fields for email and password, and buttons for login and signup.
    It checks the entered credentials against stored user data and updates the session state accordingly.
    """
    st.title("🔐 Login / Signup")
    users = load_users()
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if email in users and users[email]["password"] == password:
            st.session_state.update({
                "authenticated": True,
                "current_user": email,
                "bot_config": users[email].get("bot_config", {}),
                "uploaded_files": users[email].get("uploaded_files", []),
                "vector_store": None,  # Removed FAISS for simplicity
                "tags": users[email].get("tags", {}),
                "page": "Bot Purpose"
            })
            st.success("✅ Login successful! Redirecting...")
            st.rerun()
        else:
            st.error("❌ Invalid credentials. Please try again or sign up.")

    if st.button("Sign Up"):
        if email in users:
            st.error("❌ Email already registered. Please log in.")
        elif email and password:
            users[email] = {"password": password, "bot_config": {}, "uploaded_files": [], "tags": {}}
            save_users(users)
            st.session_state.update({
                "authenticated": True,
                "current_user": email,
                "page": "Bot Purpose"
            })
            st.success("✅ Account created successfully! Redirecting...")
            st.rerun()
        else:
            st.error("❌ Please enter a valid email and password.")

if "authenticated" in st.session_state and st.session_state.authenticated:
    bot_purpose()
