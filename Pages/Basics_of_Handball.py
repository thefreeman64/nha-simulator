import streamlit as st

# DO NOT use st.set_page_config() in subpages

# Title
st.title("🏐 Basics of Handball")

# Rules Section
st.header("📋 Rules of Handball")
st.markdown("""
Handball is a team sport derived from the classic playground game of four-square, adapted with unique competitive rules. 

- Two teams of four players compete on opposite sides of a chest-high net.
- The court measures **15 by 7 meters**, divided by the net at the center.
- A match starts with the **Lineman** serving from the back line.
- Teams score **1 point** by bouncing the ball into the opponent's rectangle and then causing it to land anywhere **outside** that area.
- Games are played to **21 points**, but:
  - If tied at 20–20, win condition increases to 22.
  - If tied again at 21–21, it moves to 23, and so on.
""")

# Positions Section
st.header("🧍 Player Positions")
st.markdown("""
Each team fields **four players**, each with a specific role. While roles are flexible, here's the general breakdown:

- **Forwards (2 players):**  
  Positioned at the net. Their main objective is scoring.  
  - *Main Forward*: Usually tall and aggressive, excels in smashing and net control.  
  - *Secondary Forward*: Often more tactical, combining offensive and defensive duties.

- **Center:**  
  Stays near the backline. Acts as the **playmaker**, setting up attacks and assisting forwards.  
  Also supports in rebounds and transitions.

- **Lineman:**  
  The key **defender and rebounder**. Typically the player who serves.  
  Strong and agile, often interchangeable with the Center role.

> 📝 *Note: Roles are fluid, and players often switch based on skills and strategy.*
""")