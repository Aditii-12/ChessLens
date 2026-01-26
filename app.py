import streamlit as st
import base64
import subprocess
import database as db
import os
import pandas as pd
import json
from streamlit_autorefresh import st_autorefresh

st_autorefresh(interval=5000, key="json_refresh")

def set_bg(png_file):
    with open(png_file, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded}");
        background-size: cover;
        background-position: center;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

set_bg("assets/this.jpeg")
db.init_db("data/users.db")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None
if "played" not in st.session_state:
    st.session_state.played = False

st.sidebar.title("🔑 Authentication")
auth_choice = st.sidebar.selectbox("Choose", ["Login", "Sign Up", "Logout"])

st.markdown("<h1>♟ ChessLens</h1>", unsafe_allow_html=True)

if auth_choice == "Login" and not st.session_state.logged_in:
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")
    if st.button("Login"):
        if db.login_user(u, p):
            st.session_state.logged_in = True
            st.session_state.username = u
            st.rerun()
        else:
            st.error("Invalid credentials")

elif auth_choice == "Sign Up":
    u = st.text_input("New Username")
    p = st.text_input("Password", type="password")
    if st.button("Sign Up"):
        st.success(db.add_user(u, p))

elif auth_choice == "Logout":
    st.session_state.logged_in = False
    st.session_state.played = False

if st.session_state.logged_in:
    st.success(f"Welcome {st.session_state.username}")
    if st.button("▶ Play"):
        subprocess.Popen(["python3", "mouse.py"])
        st.session_state.played = True

    if st.session_state.played:
        if os.path.exists("data/ready.flag"):
            with open("data/chess_analysis.json") as f:
                data = json.load(f)
            for k, v in data.items():
                st.subheader(k)
                st.table(pd.DataFrame(v["best_moves"]))
                st.write("Future:", v["future_moves"])
