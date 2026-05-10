import streamlit as st
import base64
import subprocess
import sys
import database as db
import os
import pandas as pd
import json
from streamlit_autorefresh import st_autorefresh

# ✅ FIX 1: Ensure required directories exist on fresh clone (prevents crash)
os.makedirs("data", exist_ok=True)
os.makedirs("assets/moves", exist_ok=True)

# Auto refresh every 5 seconds
st_autorefresh(interval=5000, key="json_refresh")

# === Background setup ===
def set_bg(png_file):
    # ✅ FIX 2: Guard against missing background image instead of crashing
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
        background-position: center;
    }}
    .title-text, .login-text, label, .stMarkdown p {{
        color: white !important;
        font-weight: bold;
        -webkit-text-stroke: 1px black;
        text-shadow: 1px 1px 2px black;
    }}
    .stButton>button {{
        background-color: #5BBC2E !important;
        color: white !important;
        border-radius: 8px;
        font-weight: bold;
    }}
    label {{
        font-size: 2rem !important;
        font-weight: bold !important;
        color: white !important;
        -webkit-text-stroke: 0.5px black;
        text-shadow: 1px 1px 2px black;
    }}
    .welcome-text {{
        font-size: 2rem !important;
        font-weight: bold !important;
        color: white !important;
        -webkit-text-stroke: 1px black;
        text-shadow: 1px 1px 2px black;
    }}
    .stTable table {{ background-color: black !important; color: white !important; }}
    .stTable th {{ color: white !important; background-color: #222 !important; }}
    .stTable td {{ color: white !important; background-color: #111 !important; }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

set_bg("assets/this.jpeg")

# === Initialize DB ===
db.init_db("data/users.db")

# === Session state init ===
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None
if "played" not in st.session_state:
    st.session_state.played = False

# === Sidebar ===
st.sidebar.title("🔑 Authentication")
auth_choice = st.sidebar.selectbox("Choose an option:", ["Login", "Sign Up", "Logout"])

st.markdown('<h1 class="title-text">♟ Chess Dashboard</h1>', unsafe_allow_html=True)

# === Auth logic ===
if auth_choice == "Login" and not st.session_state.logged_in:
    st.markdown('<h3 class="login-text">Login to Your Account</h3>', unsafe_allow_html=True)
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = db.login_user(username, password)
        if user:
            st.success("Login Successful ✅")
            st.session_state.logged_in = True
            st.session_state.username = username
            st.rerun()
        else:
            st.error("Invalid credentials ❌")

elif auth_choice == "Sign Up" and not st.session_state.logged_in:
    st.markdown('<h3 class="login-text">Create a New Account</h3>', unsafe_allow_html=True)
    new_user = st.text_input("New Username")
    new_pass = st.text_input("New Password", type="password")
    confirm_pass = st.text_input("Confirm Password", type="password")
    if st.button("Sign Up"):
        if new_pass == confirm_pass and new_user.strip() != "":
            result = db.add_user(new_user, new_pass, profile="standard")
            if "successfully" in result:
                st.success("Account Created 🎉 You can now login!")
            else:
                st.error(result)
        else:
            st.error("Passwords do not match ❌")

elif auth_choice == "Logout":
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.played = False
    st.success("You have been logged out!")

# === Logged-in dashboard ===
if st.session_state.logged_in:
    st.markdown(
        f'<label class="welcome-text">Welcome, {st.session_state.username} 🎉</label>',
        unsafe_allow_html=True
    )

    if st.button("▶ Play"):
        st.success("Launching game...")
        # ✅ FIX 3: Use sys.executable so runner.py runs inside the same venv
        subprocess.Popen([sys.executable, "runner.py"])
        st.session_state.played = True

    if st.session_state.played:
        json_file = "data/chess_analysis.json"
        flag_file = "data/ready.flag"

        if os.path.exists(flag_file) and os.path.exists(json_file):
            # ✅ FIX 4: Guard against empty/malformed JSON written mid-process
            try:
                with open(json_file, "r") as f:
                    content = f.read().strip()
                if not content or content == "{}":
                    st.info("⏳ Analysis in progress, please wait...")
                else:
                    data = json.loads(content)
                    st.subheader("Best Move Analysis")

                    fen_labels = {"Current_FEN": "White", "Flipped_FEN": "Black"}

                    for fen_type, fen_data in data.items():
                        label = fen_labels.get(fen_type, fen_type.replace("_", " "))
                        st.markdown(f"### {label}")

                        if fen_data.get("best_moves"):
                            df_best = pd.DataFrame(fen_data["best_moves"])
                            st.table(df_best)

                        if fen_data.get("future_moves"):
                            moves_str = ", ".join(fen_data["future_moves"])
                            st.markdown(
                                f"""<div style="background-color:white;color:black;
                                padding:10px;border-radius:5px;font-weight:bold;">
                                <strong>Future Moves:</strong> {moves_str}</div>""",
                                unsafe_allow_html=True
                            )
                        st.markdown("---")
            except json.JSONDecodeError:
                st.info("⏳ Waiting for analysis to complete...")
        else:
            st.info("⏳ Waiting for game analysis... (Make a palm-open gesture to trigger)")