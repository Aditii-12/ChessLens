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
    if not os.path.exists(png_file):
        return
    with open(png_file, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded}");
        background-size: cover;
    }}
    .block-container {{
        background: rgba(0,0,0,0.55);
        border-radius: 16px;
        padding: 2rem;
    }}
    h1,h2,h3,p,label {{ color:white; }}
    .stButton>button {{
        background:#4CAF50;
        color:white;
        font-weight:bold;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

set_bg("assets/this.jpeg")
db.init_db("data/users.db")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "played" not in st.session_state:
    st.session_state.played = False

st.title("♟ ChessLens")

if not st.session_state.logged_in:
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")
    if st.button("Login"):
        if db.login_user(u, p):
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Invalid credentials")
else:
    st.success("Logged in")

    if st.button("▶ Play"):
        subprocess.Popen(["python3", "runner.py"])
        st.session_state.played = True

    if st.session_state.played:
        if os.path.exists("data/ready.flag") and os.path.exists("data/chess_analysis.json"):
            with open("data/chess_analysis.json") as f:
                data = json.load(f)

            st.subheader("Best Move Analysis")
            for k, v in data.items():
                st.markdown(f"### {k}")
                st.table(pd.DataFrame(v["best_moves"]))
