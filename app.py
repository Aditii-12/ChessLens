import streamlit as st
from database import init_db, login_user

# initialize database
init_db()

st.set_page_config(page_title="ChessLens", layout="wide")

st.title("♟ ChessLens")
st.write("ChessLens dashboard — under development")

st.sidebar.title("Controls")
st.sidebar.subheader("Login")

username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")

if st.sidebar.button("Sign In"):
    user = login_user(username, password)
    if user:
        st.sidebar.success(f"Welcome, {username}")
    else:
        st.sidebar.error("Invalid username or password")

st.sidebar.divider()
st.sidebar.button("Capture Screenshot")
st.sidebar.button("Analyze Position")
