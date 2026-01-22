import streamlit as st
from database import init_db, login_user, add_user

# Initialize database
init_db()

st.set_page_config(page_title="ChessLens", layout="wide")

# Main content
st.title("♟ ChessLens")
st.write("ChessLens dashboard — under development")

# Sidebar
st.sidebar.title("Controls")
st.sidebar.subheader("Authentication")

username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")

# Horizontal buttons
col1, col2 = st.sidebar.columns(2)

login_clicked = col1.button("Sign In")
signup_clicked = col2.button("Sign Up")

if login_clicked:
    user = login_user(username, password)
    if user:
        st.sidebar.success(f"Welcome, {username}")
    else:
        st.sidebar.error("Invalid username or password")

if signup_clicked:
    if add_user(username, password):
        st.sidebar.success("Account created. You can sign in now.")
    else:
        st.sidebar.error("Username already exists")


st.sidebar.divider()

# Placeholder controls
st.sidebar.button("Capture Screenshot")
st.sidebar.button("Analyze Position")
