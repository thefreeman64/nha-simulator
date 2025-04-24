import streamlit as st

st.set_page_config(
    page_title="National Handball Association",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.markdown("<h1 style='text-align: center;'>Welcome to the National Handball Association!</h1>", unsafe_allow_html=True)

st.write("""
The National Handball Association is a fictional sports league inspired by a love for handball and the NBA.
Explore the Basics of Handball and try the Betting Simulator using the navigation on the left.
""")