import streamlit as st
from database import init_db, login_user, add_user
from screen_shot import capture_screen
from engine import analyze_fen

# Initialize database
init_db()

st.set_page_config(page_title="ChessLens", layout="wide")

# ---------- SESSION STATE ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None

# ---------- MAIN UI ----------
st.title("♟ ChessLens")
st.write("ChessLens dashboard — under development")

st.sidebar.title("Controls")

# ---------- AUTH SECTION ----------
if not st.session_state.logged_in:
    st.sidebar.subheader("Authentication")

    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    col1, col2 = st.sidebar.columns(2)
    login_clicked = col1.button("Sign In")
    signup_clicked = col2.button("Sign Up")

    if login_clicked:
        user = login_user(username, password)
        if user:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.sidebar.success(f"Welcome, {username}")
            st.rerun()
        else:
            st.sidebar.error("Invalid username or password")

    if signup_clicked:
        if add_user(username, password):
            st.sidebar.success("Account created. You can sign in now.")
        else:
            st.sidebar.error("Username already exists")

# ---------- DASHBOARD ----------
else:
    st.sidebar.success(f"Logged in as {st.session_state.username}")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.rerun()

    st.sidebar.divider()

    if st.sidebar.button("Capture Screenshot"):
        path = capture_screen()
        st.success("Screenshot captured")
        st.image(path, caption="Captured Screenshot")

    st.sidebar.button("Analyze Position")

    st.info("More analysis features will be added here.")

st.subheader("Manual FEN Input")

fen_input = st.text_area(
    "Paste FEN here",
    placeholder="e.g. rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
)

if fen_input:
    st.code(fen_input, language="text")
    results = analyze_fen(fen_input)
    

