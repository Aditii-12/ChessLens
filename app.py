import streamlit as st
from database import init_db, login_user, add_user
from screen_shot import capture_screen
from engine import analyze_fen

st.set_page_config(
    page_title="ChessLens",
    layout="wide"
)

init_db()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None

st.title("♟ ChessLens")
st.caption("ChessLens dashboard — under development")

st.sidebar.title("Controls")

if not st.session_state.logged_in:
    st.sidebar.subheader("Authentication")

    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    col1, col2 = st.sidebar.columns(2)
    login_clicked = col1.button("Sign In")
    signup_clicked = col2.button("Sign Up")

    if login_clicked:
        if not username.strip() or not password.strip():
            st.sidebar.error("Username and password cannot be empty ❌")
        else:
            user = login_user(username, password)
            if user:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.sidebar.success(f"Welcome, {username} 🎉")
                st.rerun()
            else:
                st.sidebar.error("Invalid username or password ❌")

    if signup_clicked:
        if not username.strip() or not password.strip():
            st.sidebar.error("Username and password cannot be empty ❌")
        else:
            result = add_user(username, password)
            if "successfully" in result.lower():
                st.sidebar.success("Account created! You can sign in now ✅")
            else:
                st.sidebar.error(result)

else:
    st.sidebar.success(f"Logged in as {st.session_state.username}")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.rerun()

    st.sidebar.divider()

    if st.sidebar.button("Capture Screenshot"):
        try:
            path = capture_screen()
            st.success("Screenshot captured 📸")
            st.image(path, caption="Captured Screenshot")
        except Exception as e:
            st.error(f"Screenshot failed: {e}")

    st.info("More automation & gesture features will be added here.")


st.subheader("Manual FEN Input")

fen_input = st.text_area(
    "Paste FEN here",
    placeholder="e.g. rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
)

analyze_clicked = st.button("Analyze FEN")

if analyze_clicked:
    if not fen_input.strip():
        st.warning("Please enter a FEN string ⚠️")
    elif len(fen_input.split()) < 4:
        st.error("Invalid FEN format ❌")
    else:
        try:
            with st.spinner("Analyzing position with Stockfish ♟️"):
                results = analyze_fen(fen_input)

            if not results:
                st.warning("No analysis returned.")
            else:
                st.subheader("Best Moves")
                for r in results:
                    st.write(f"**{r['move']}** — {r['score']}")

        except Exception as e:
            st.error(f"Analysis failed: {e}")
