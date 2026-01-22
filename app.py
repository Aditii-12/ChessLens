import streamlit as st
from database import init_db, login_user, add_user

# Initialize DB
init_db()

st.set_page_config(page_title="ChessLens", layout="wide")

st.title("♟ ChessLens")
st.write("ChessLens dashboard — under development")

st.sidebar.title("Controls")

# Toggle between Login / Sign Up
mode = st.sidebar.radio("Auth Mode", ["Login", "Sign Up"])

username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")

if mode == "Login":
    if st.sidebar.button("Sign In"):
        user = login_user(username, password)
        if user:
            st.sidebar.success(f"Welcome, {username}")
        else:
            st.sidebar.error("Invalid username or password")

else:  # Sign Up
    if st.sidebar.button("Create Account"):
        ok = add_user(username, password)
        if ok:
            st.sidebar.success("Account created. You can log in now.")
        else:
            st.sidebar.error("Username already exists")

st.sidebar.divider()
st.sidebar.button("Capture Screenshot")
st.sidebar.button("Analyze Position")
