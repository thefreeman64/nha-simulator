import streamlit as st

st.set_page_config(page_title="National Handball Association", layout="centered")

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to:", ["Home", "Basics of Handball", "Betting Simulator"])

# Page Routing
if page == "Home":
    st.markdown("<h1 style='text-align: center; font-size: 48px;'>Welcome to the National Handball Association!</h1>", unsafe_allow_html=True)

    st.markdown("""
    <div style='text-align: center; font-size: 18px;'>
    The National Handball Association is a fake sports league based off of the semi-fake sport of handball. This project was created by me about two years ago inspired by a love for sports and my then-new interest in the NBA, which this fake league is very much based off of. 
    
    In this, you can explore the basics of handball, the history of the NHA, the different teams and how they are doing today, and a betting simulator which will allow you to bet on teams to win the championship, randomized every time you simulate it.
    </div>
    """, unsafe_allow_html=True)

elif page == "Basics of Handball":
    st.title("The Basics of Handball")
    st.write("Coming soon: A guide to handball rules and strategies.")

elif page == "Betting Simulator":
    st.title("Betting Simulator")
    st.write("Coming soon: Bet on NHA teams to win the championship!")