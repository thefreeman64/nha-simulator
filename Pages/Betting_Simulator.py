import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Betting Simulator", layout="centered")

from simulator import (
    simulate_season,
    simulate_playoffs,
    draw_nba_bracket,
    calculate_odds,
)

# Utility function to flatten nested team lists
def extract_teams(bracket_side):
    team_set = set()
    for item in bracket_side:
        if isinstance(item, (list, tuple)):
            for subitem in item:
                if isinstance(subitem, (list, tuple)):
                    team_set.update(subitem)
                else:
                    team_set.add(subitem)
        else:
            team_set.add(item)
    return list(team_set)

# Format display of teams with stats and odds
def format_team_display(name, stats, seed):
    odds = calculate_odds(name, seed)
    odds_pct = 100 / odds if odds > 0 else 0
    return f"{seed}. {name} ({stats['W']} W - {stats['L']} L, {odds_pct:.1f}% to win)"

def run_simulation():
    st.set_page_config(layout="wide")
    st.title("NHA Season & Playoff Simulator")

    # Initialize session state
    for key in ["standings", "bracket_data", "east_top", "west_top", "final_champion", "final_bracket"]:
        if key not in st.session_state:
            st.session_state[key] = None

    # Simulate regular season
    if st.button("Start Simulation"):
        with st.spinner("Simulating regular season..."):
            eastern_teams = [
                "New England Captains", "Atlanta Strikers", "New York Skies", "The Nashville Folk",
                "Miami Savages", "New York Freemen", "Detroit Veterans", "Charlotte Vipers",
                "Chicago Phantoms", "Toronto Speedsters", "Montreal Franks", "Pennsylvania Dutchman"
            ]
            western_teams = [
                "San Francisco Money", "Salt Lake Spices", "Los Angeles Cheetahs", "California Goblins",
                "Denver Titans", "Oregon Tellers", "Seattle Ringers", "Dallas Hunchbacks",
                "Houston 29ers", "Phoenix Rosebuds", "Omaha Crows", "Minneapolis Hunters"
            ]

            standings, bracket_data, _ = simulate_season(eastern_teams, western_teams)
            st.session_state.standings = standings
            st.session_state.bracket_data = bracket_data
            st.session_state.east_top = extract_teams(bracket_data["east"])
            st.session_state.west_top = extract_teams(bracket_data["west"])
            st.session_state.final_champion = None
            st.session_state.final_bracket = None

            st.success("Regular season completed.")

    # Display standings and betting options
    if st.session_state.standings:
        standings_dict = {team["name"]: team for team in st.session_state.standings}
        east_results = {team: standings_dict[team] for team in st.session_state.east_top}
        west_results = {team: standings_dict[team] for team in st.session_state.west_top}

        st.subheader("🏆 Top 8 Teams Per Conference")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Eastern Conference")
            sorted_east = sorted(east_results.items(), key=lambda x: x[1]["W"], reverse=True)
            for i, (team, stats) in enumerate(sorted_east, start=1):
                st.write(format_team_display(team, stats, seed=i))

        with col2:
            st.markdown("### Western Conference")
            sorted_west = sorted(west_results.items(), key=lambda x: x[1]["W"], reverse=True)
            for i, (team, stats) in enumerate(sorted_west, start=1):
                st.write(format_team_display(team, stats, seed=i))

        # Betting UI
        st.subheader("💰 Place Your Bet!")
        playoff_teams = st.session_state.east_top + st.session_state.west_top
        bet_team = st.selectbox("Pick a team to bet on:", playoff_teams)
        seed = playoff_teams.index(bet_team) + 1
        odds = calculate_odds(bet_team, seed)
        st.write(f"**Bet Odds for {bet_team}: x{odds} payout**")
        bet_amount = st.number_input(f"How much do you want to bet on {bet_team}?", min_value=0.0, step=1.0)

        # Simulate Playoffs
        if st.button("Simulate Playoffs"):
            with st.spinner("Simulating playoffs..."):
                final_matchup, final_champion, final_bracket = simulate_playoffs(
                    st.session_state.east_top, st.session_state.west_top
                )
                st.session_state.final_champion = final_champion
                st.session_state.final_bracket = final_bracket
                st.success(f"The champion is **{final_champion}**!")

            if final_champion == bet_team:
                winnings = round(bet_amount * odds, 2)
                st.balloons()
                st.success(f"You won your bet on **{final_champion}**! You earned ${winnings} (Odds: x{odds})")
            else:
                st.error(f"Your bet on {bet_team} did not win. You lost ${bet_amount}.")

            # Draw final bracket
            with st.spinner("Drawing playoff bracket..."):
                fig = draw_nba_bracket(
                    final_bracket["east"],
                    final_bracket["west"],
                    final_bracket["final"],
                    highlight_team=bet_team
                )
                st.pyplot(fig)

if __name__ == "__main__":
    run_simulation()