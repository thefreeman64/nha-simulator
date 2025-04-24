import streamlit as st
import matplotlib.pyplot as plt
from simulator import (
    simulate_season,
    simulate_playoffs,
    draw_nba_bracket,
    calculate_odds,
)

st.set_page_config(
    page_title="National Handball Association",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Define utility functions here
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

def format_team_display(name, stats, seed, in_playoffs):
    odds = calculate_odds(name, seed)
    odds_pct = 100 / odds if odds > 0 else 0
    color = "red" if in_playoffs else "black"
    return f"<span style='color: {color};'>{seed}. {name} ({stats['W']} W - {stats['L']} L, {odds_pct:.1f}% to win)</span>"

# Title and subtext
st.markdown("<h1 style='text-align: center;'>Welcome to the National Handball Association!</h1>", unsafe_allow_html=True)

st.markdown("**What is the NHA?**")
st.markdown("""
The National Handball Association is a fake sports league based off of the semi-fake sport of handball. This project was created by me about two years ago inspired by love for sports and my then-new interest in the NBA, which this fake league is very much based off of. The goal of this installation was to present an in-depth exploration of the NHA plus a fake betting league you can interact with, however this was not possible so I only have here provided the fake betting league.
""")

st.title("NHA Season & Playoff Simulator")

# Place the "Start Simulation" button directly under the header
if st.button("Start Simulation"):
    with st.spinner("Simulating regular season..."):
        eastern_teams = [
            "New York Skies", "New England Captains", "Toronto Speedsters", "Detroit Veterans",
            "The Nashville Folk", "Miami Savages", "Charlotte Vipers", "Chicago Phantoms",
            "New York Freemen", "Atlanta Strikers", "Montreal Franks", "Pennsylvania Dutchman"
        ]
        western_teams = [
            "Salt Lake Spices", "Los Angeles Cheetahs", "San Francisco Money", "Dallas Hunchbacks",
            "California Goblins", "Houston 29ers", "Oregon Tellers", "Denver Titans",
            "Seattle Ringers", "Minneapolis Hunters", "Phoenix Rosebuds", "Omaha Crows"
        ]

        standings, bracket_data, _ = simulate_season(eastern_teams, western_teams)
        st.session_state.standings = standings
        st.session_state.bracket_data = bracket_data
        st.session_state.east_top = extract_teams(bracket_data["east"])
        st.session_state.west_top = extract_teams(bracket_data["west"])
        st.session_state.final_champion = None
        st.session_state.final_bracket = None

        st.success("Regular season completed!")

# Display standings and betting options
if "standings" in st.session_state and st.session_state.standings:
    standings_dict = {team["name"]: team for team in st.session_state.standings}
    east_results = {team: standings_dict[team] for team in standings_dict if standings_dict[team]["conference"] == "East"}
    west_results = {team: standings_dict[team] for team in standings_dict if standings_dict[team]["conference"] == "West"}

    st.subheader("🏆 Regular Season Results")
    st.markdown("_Red = Playoffs_")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Eastern Conference")
        sorted_east = sorted(east_results.items(), key=lambda x: x[1]["W"], reverse=True)
        for i, (team, stats) in enumerate(sorted_east, start=1):
            in_playoffs = team in st.session_state.east_top
            st.markdown(format_team_display(team, stats, seed=i, in_playoffs=in_playoffs), unsafe_allow_html=True)

    with col2:
        st.markdown("### Western Conference")
        sorted_west = sorted(west_results.items(), key=lambda x: x[1]["W"], reverse=True)
        for i, (team, stats) in enumerate(sorted_west, start=1):
            in_playoffs = team in st.session_state.west_top
            st.markdown(format_team_display(team, stats, seed=i, in_playoffs=in_playoffs), unsafe_allow_html=True)

    # Betting UI
    st.subheader("💰 Place Your Bet!")
    playoff_teams = st.session_state.east_top + st.session_state.west_top
    bet_team = st.selectbox("Pick a team to bet on:", playoff_teams)
    seed = playoff_teams.index(bet_team) + 1
    odds = calculate_odds(bet_team, seed)
    st.write(f"**Bet Odds for {bet_team}: x{odds} payout**")
    bet_amount = st.number_input(f"How much do you want to bet on {bet_team}?", min_value=0.0, step=1.0)

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

        # Display the playoff bracket after betting
        if "final_bracket" in st.session_state and st.session_state.final_bracket:
            st.subheader("🏆 Playoff Bracket")
            with st.spinner("Drawing playoff bracket..."):
                fig = draw_nba_bracket(
                    st.session_state.final_bracket["east"],
                    st.session_state.final_bracket["west"],
                    st.session_state.final_bracket["final"],
                    highlight_team=None
                )
                st.pyplot(fig, use_container_width=True)

# Team Info Section
st.subheader("**Team Info**")
team_col1, team_col2 = st.columns(2)

with team_col1:
    st.markdown("### **Eastern Conference**")
    st.markdown("**🌃 New York Skies**")
    st.markdown("""
    The New York Skies are the new hot team on the block. After drafting Luis Morales with the first overall pick in 2020 and watching him become a superstar, then acquiring the already made superstar Dennis Campbell in 2022, the team has grown to become an unstoppable force in the future, hopefully being able to break the New York Skies’ playoff woes that have existed since their foundation in 1991.
    """)
    st.markdown("**🏴‍☠️ New England Captains**")
    st.markdown("""
    Last year’s champions, the New England Captains are probably the scariest team around. Their superstar, now three-time MVP David Garcia, is an unstoppable force in the league and pairing him up with extremely high-level talent such as Anthony Colombo and Amir Bracken makes this team an enormous threat. It is said to be extremely difficult to go back-to-back in this league, though.
    """)
    st.markdown("**🚀 Toronto Speedsters**")
    st.markdown("""
    A new-ish team on the block, after having made the conference finals in 2022, haven’t been able to reach that same level again. But their star Aaron Telugu is only 25 years old at this point and Ukrainian lineman Sergei Ivanov just made his first all-star appearance this year, so Toronto is a team that will always be a threat, even if they are still young.
    """)
    st.markdown("**🏅 Detroit Veterans**")
    st.markdown("""
    Detroit is a very interesting team: led by three-time all-star center Devon Lee and two-time all-star forward Drew Wallace, they were able to make the conference finals last year, but it is impossible to predict if they could do it again. They have just as much chance of winning the championship as they do crashing out in the first round.
    """)
    st.markdown("**🎻 The Nashville Folk**")
    st.markdown("""
    Led by first overall pick in the 2022 draft Damian Potter and recent all-star Roland Goldbridge, The Nashville Folk is in a similar vein as Detroit. Nashville is probably the most well-rounded and average team in the league, meaning they will probably find themselves middle of the pack most times.
    """)
    st.markdown("**🔥 Miami Savages**")
    st.markdown("""
    What happened to the Miami Savages is sad. During star center Russell White’s prime, as he won two MVP awards, they were only able to go to the finals once and faced Charlie Wilson, a man on a mission. Now, Russell is getting old, and his supporting cast is either incompetent or leaving to play for better teams. You can never count out Miami just due to how talented Russell is, but it is harder and harder to believe in them.
    """)
    st.markdown("**🐍 Charlotte Vipers**")
    st.markdown("""
    One of the regularly worst teams in the league, the Charlotte Vipers lost their greatest player 5 years ago. After a couple seasons at the bottom of the league, Charlotte received the 1st overall pick in the 2023 draft, using it to select generational UCLA talent Kevin Marquez-Smith, who is already a two-time all-star in his first two seasons and is hungry for a little playoff experience, despite his young age of 21.
    """)
    st.markdown("**👻 Chicago Phantoms**")
    st.markdown("""
    Chicago is one of those teams with no real direction. They acquired George Brecht at the trade deadline to pair up with 2023 rookie of the year Horace Lue, but George is now very old, and Lue does not seem to have the hype he used to. Chicago is definitely a threat to make it into the playoffs, but that’s probably about it.
    """)
    st.markdown("**🗽 New York Freemen**")
    st.markdown("""
    Led by two-time all-star Andrew James, the Freemen are a team that, at the moment, are basically one for two for seasons in the playoffs. No one expects them to make any kind of deep run, however there is still a 50/50 chance that they’ll make it in.
    """)
    st.markdown("**⚡ Atlanta Strikers**")
    st.markdown("""
    The Strikers are lucky to have 2023 Court Protector of the Year winner Darnell Simpson, however his injury record and the lack of supporting cast around him makes it so that Atlanta usually falls towards the bottom of Eastern Conference standing predictions. You never know what they could do, but it's most likely they will miss the playoffs.
    """)
    st.markdown("**🍁 Montreal Franks**")
    st.markdown("""
    Since the loss of 2017 MVP and 2018 champion Adrian Dragan to the Los Angeles Cheetahs in the 2023 off-season, nothing at all is expected for the Montreal Franks. Most likely they bottom out for the next couple years for some draft capital, and don’t make any appearances in the playoffs soon.
    """)
    st.markdown("**🛡️ Pennsylvania Dutchman**")
    st.markdown("""
    The Pennsylvania Dutchman are a complete lost cause. Five-time all-star Dell Cooper is their most recent “star” (if you can even call him that), but apart from leading the Dutchman to the conference finals in 2017 he hasn’t done much. Now, he is old and injury prone, and there is absolutely no hope for this team.
    """)

with team_col2:
    st.markdown("### **Western Conference**")
    st.markdown("**🌶️ Salt Lake Spices**")
    st.markdown("""
    The Salt Lake Spices are one of the most dangerous teams in the entire NHA. Already having 2018 MVP Harald Johansson, the Spices acquired former 2021 MVP and one-time champion J’akkar Okoro in the 2024 off-season, creating one of the greatest backline defenses in NHA history.
    """)
    st.markdown("**🐆 Los Angeles Cheetahs**")
    st.markdown("""
    After winning the championship in 2023, the Los Angeles Cheetahs lost one of their biggest stars and arguably one of the greatest players of all time, Alexander Klein, and with their young star Donald Casimaty and his stellar supporting cast consisting of former champion and 6x all-star Joseph Maka, ex-superstar Adrian Dragan and 4x all-star Jon Hackman they are one of the biggest threats in the west.
    """)
    st.markdown("**💰 San Francisco Money**")
    st.markdown("""
    Led by super-star recipient of the 2024 MVP Lionel Cruz, paired up with former Dallas Hunchbacks legend Gordon Ryker and all-star German forward Tycho Behrens, the San Francisco Money are always a threat to watch out for, however Cruz is known for coming up short when it matters most.
    """)
    st.markdown("**🦌 Dallas Hunchbacks**")
    st.markdown("""
    A young team, the Hunchbacks have a couple good pieces around their 24-year-old all-star center Phil Funkleder, however this is the first season in a couple years that they have been in the upper echelon of the NHA, making them pretty inexperienced, but very talented, nonetheless.
    """)
    st.markdown("**👹 California Goblins**")
    st.markdown("""
    The Goblins are historically known for their incompetence as a franchise (save for their miracle championship in 2007), however after having acquired forward Willo Di Matteo from the New England Captains in 2022, they have mounted up a decent squad that could threaten a deep run in the playoffs.
    """)
    st.markdown("**🚀 Houston 29ers**")
    st.markdown("""
    Coming off the back of a conference finals appearance last year, the Houston 29ers are always a threat. Led by their two stars, Mikael Joyce and Alan Walker, Houston is a tough team that cannot be underestimated.
    """)
    st.markdown("**📜 Oregon Tellers**")
    st.markdown("""
    Next to the Goblins, the Tellers are one of the saddest franchises in NHA history. The grand return of Colson Berger, their greatest ever player, in 2023, was a nice gesture, however he is aging and while getting into the playoffs is a possibility they are nowhere near being able to win a championship.
    """)
    st.markdown("**🗻 Denver Titans**")
    st.markdown("""
    With the first overall pick in the 2021 draft, the Denver Titans selected Monte French, and while the forward is still very young at 23 years old, this is a team who has the potential to make it into the playoffs. Further than that, they will need luck on their side.
    """)
    st.markdown("**🔔 Seattle Ringers**")
    st.markdown("""
    Seattle is a team that has never really had a lot of luck. Despite getting the first overall pick in 2017, the player they chose with that pick, Leo Mendes, hasn’t been able to live up to expectations like they’ve expected, and they consistently underperform compared to their expectations every year.
    """)
    st.markdown("**🏹 Minneapolis Hunters**")
    st.markdown("""
    There’s not much to expect this year from the Minneapolis Hunters, who had the first overall pick last year and used it to select University of Virginia star Christian Murray, however the emergence of Bart Salaja as a good second option proves hope for the future.
    """)
    st.markdown("**🌹 Phoenix Rosebuds**")
    st.markdown("""
    After Charlie Wilson, one of the greatest players of all time, brought a championship to Phoenix in 2022, the Rosebuds were on top of the world. However, after his departure from the team to play back in his home country of Australia the next year, they have no real identity and will most likely be found at the bottom of the table.
    """)
    st.markdown("**🦅 Omaha Crows**")
    st.markdown("""
    The Omaha Crows are one of the greatest franchises in NHA history, mainly due to Rick Harrison’s status as the greatest coach to ever do it, but after his retirement in 2021, the team would start to fall apart, with the final piece being J’akkar Okoro’s move to Salt Lake City last off-season, that would completely kill any chance this team would have at winning games.
    """)

if __name__ == "__main__":
    run_simulation()