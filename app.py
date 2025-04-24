import streamlit as st

# Set the app config — this enables the sidebar
st.set_page_config(
    page_title="National Handball Association",
    layout="centered",
    initial_sidebar_state="expanded"  # 👈 This makes sure the sidebar shows up
)

# Home page content
st.markdown("<h1 style='text-align: center; font-size: 48px;'>Welcome to the National Handball Association!</h1>", unsafe_allow_html=True)

st.markdown("""
<div style='text-align: center; font-size: 18px;'>
The National Handball Association is a fake sports league based off of the semi-fake sport of handball. This project was created by me about two years ago inspired by a love for sports and my then-new interest in the NBA, which this fake league is very much based off of. 

In this, you can explore the basics of handball, the history of the NHA, the different teams and how they are doing today, and a betting simulator which will allow you to bet on teams to win the championship, randomized every time you simulate it.
</div>
""", unsafe_allow_html=True)