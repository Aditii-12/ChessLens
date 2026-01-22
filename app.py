import streamlit as st

st.set_page_config(page_title="ChessLens", layout="wide")

# Main title
st.title("♟ ChessLens")
st.write("ChessLens dashboard — under development")

# Sidebar
st.sidebar.title("Controls")

# Login UI
st.sidebar.subheader("Login")

username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")

if st.sidebar.button("Sign In"):
    st.sidebar.success("Login clicked (logic coming next)")

# Placeholder buttons
st.sidebar.divider()
st.sidebar.button("Capture Screenshot")
st.sidebar.button("Analyze Position")
