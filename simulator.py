import streamlit as st
import random
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# ===== TEAM DATA =====
tiers = {
    "A": ["New York Skies", "New England Captains", "Salt Lake Spices", "Los Angeles Cheetahs"],
    "B": ["Toronto Speedsters", "Detroit Veterans", "The Nashville Folk", "Miami Savages",
          "Dallas Hunchbacks", "San Francisco Money", "California Goblins", "Houston 29ers"],
    "C": ["Charlotte Vipers", "Chicago Phantoms", "Oregon Tellers", "Denver Titans", "New York Freemen",
          "Seattle Ringers", "Atlanta Strikers", "Minneapolis Hunters"],
    "D": ["Montreal Franks", "Pennsylvania Dutchman", "Phoenix Rosebuds", "Omaha Crows"]
}

def generate_teams():
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
    return eastern_teams, western_teams

def get_tier(team):
    for tier, team_list in tiers.items():
        if team in team_list:
            return tier
    return "C"

# ===== SIMULATION LOGIC =====

def simulate_game(team1, team2):
    tier1, tier2 = get_tier(team1), get_tier(team2)
    strength = {"A": 4, "B": 3, "C": 2, "D": 1}
    prob1 = strength[tier1] / (strength[tier1] + strength[tier2])
    return team1 if random.random() < prob1 else team2

def simulate_regular_season(teams):
    results = {team: {"W": 0, "L": 0, "Points": 0, "conference": "East" if i < 12 else "West"} 
               for i, team in enumerate(teams)}
    for _ in range(2):
        for i in range(len(teams)):
            for j in range(i + 1, len(teams)):
                team1, team2 = teams[i], teams[j]
                winner = simulate_game(team1, team2)
                loser = team2 if winner == team1 else team1
                results[winner]["W"] += 1
                results[winner]["Points"] += 3
                results[loser]["L"] += 1
    return results

def get_standings(results):
    return sorted(
        [{"name": team, **data} for team, data in results.items()],
        key=lambda x: (-x["Points"], x["name"])
    )

def simulate_series(team1, team2, best_of=9):
    wins = {team1: 0, team2: 0}
    while wins[team1] < (best_of // 2 + 1) and wins[team2] < (best_of // 2 + 1):
        winner = simulate_game(team1, team2)
        wins[winner] += 1
    return team1 if wins[team1] > wins[team2] else team2

def playoff_round(teams):
    round_matches = []
    winners = []
    for i in range(len(teams) // 2):
        team1, team2 = teams[i], teams[-(i + 1)]
        winner = simulate_series(team1, team2)
        round_matches.append((team1, team2, winner))
        winners.append(winner)
    return round_matches, winners

def simulate_playoffs(east, west):
    all_rounds = []

    def simulate_side(side):
        rounds = []
        current = side
        while len(current) > 1:
            matches, current = playoff_round(current)
            rounds.append(matches)
        return rounds, current[0]

    east_rounds, east_champ = simulate_side(east)
    west_rounds, west_champ = simulate_side(west)
    final_winner = simulate_series(east_champ, west_champ)
    all_rounds.extend([east_rounds, west_rounds, [(east_champ, west_champ, final_winner)]])
    return all_rounds, final_winner, {"east": east_rounds, "west": west_rounds, "final": (east_champ, west_champ, final_winner)}

def simulate_season(eastern_teams, western_teams):
    all_teams = eastern_teams + western_teams
    results = simulate_regular_season(all_teams)
    standings = get_standings(results)

    east = [t["name"] for t in standings if t["conference"] == "East" and t["name"] in eastern_teams][:8]
    west = [t["name"] for t in standings if t["conference"] == "West" and t["name"] in western_teams][:8]

    playoff_results, champion, bracket_data = simulate_playoffs(east, west)
    return standings, bracket_data, champion

# ===== BETTING SYSTEM =====

def calculate_odds(team, seed):
    tier = get_tier(team)
    base_odds = {'A': 2.0, 'B': 3.5, 'C': 6.0, 'D': 9.0}
    odds = base_odds.get(tier, 5.0)
    if seed >= 5:
        odds *= 1.5
    elif seed >= 3:
        odds *= 1.2
    return round(odds, 2)

# ===== BRACKET DRAWING =====
def draw_nba_bracket(east_bracket, west_bracket, finals, highlight_team=None):
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle

    fig, ax = plt.subplots(figsize=(18, 10))
    ax.axis('off')

    box_w, box_h = 3, 1
    gap_y = 1.5
    round_gap_x = 4

    # Normalize function for matching
    def normalize(name):
        return name.strip().lower().replace(" ", "") if name else ""

    norm_highlight = normalize(highlight_team)

    def draw_conference(bracket, x_start, direction):
        num_rounds = len(bracket)
        team_boxes = {}

        for rnd in range(num_rounds):
            match_spacing = gap_y * (2 ** rnd)
            for i, (team1, team2, winner) in enumerate(bracket[rnd]):
                y1 = i * match_spacing * 2
                y2 = y1 + match_spacing
                x = x_start + direction * rnd * round_gap_x

                ax.add_patch(Rectangle((x, y1), box_w, box_h, fill=False))
                ax.add_patch(Rectangle((x, y2), box_w, box_h, fill=False))

                norm_team1 = normalize(team1)
                norm_team2 = normalize(team2)

                color1 = 'red' if norm_highlight == norm_team1 else 'black'
                color2 = 'red' if norm_highlight == norm_team2 else 'black'

                ax.text(x + 0.15, y1 + box_h / 2, team1, va='center', ha='left', fontsize=7, color=color1)
                ax.text(x + 0.15, y2 + box_h / 2, team2, va='center', ha='left', fontsize=7, color=color2)

                team_boxes[(rnd, i)] = (x, y1, y2)

                x0 = x + box_w if direction == 1 else x
                x1 = x0 + direction * 0.5
                ax.plot([x0, x1], [y1 + box_h / 2, y1 + box_h / 2], color='black')
                ax.plot([x0, x1], [y2 + box_h / 2, y2 + box_h / 2], color='black')
                ax.plot([x1, x1], [y1 + box_h / 2, y2 + box_h / 2], color='black')

        last_round = num_rounds - 1
        final_match = bracket[last_round][0]
        final_y = (team_boxes[(last_round, 0)][1] + team_boxes[(last_round, 0)][2]) / 2
        final_winner = final_match[2]
        final_x = team_boxes[(last_round, 0)][0]
        return final_winner, final_y, final_x, team_boxes, last_round

    # Draw East and West
    ax.text(1, 18, "Eastern Conference", fontsize=13, weight='bold')
    east_champ, y_east, x_east, east_team_boxes, east_final_round = draw_conference(east_bracket, x_start=2, direction=1)

    ax.text(29, 18, "Western Conference", fontsize=13, weight='bold', ha='right')
    west_champ, y_west, x_west, west_team_boxes, west_final_round = draw_conference(west_bracket, x_start=28 - box_w, direction=-1)

    # Conference Champion Labels
    def place_conference_label(team_boxes, final_round, champ_name):
        finals = [v for k, v in team_boxes.items() if k[0] == final_round]
        if len(finals) >= 2:
            finals.sort(key=lambda b: b[1])
            left, right = finals[0], finals[1]
            label_x = (left[0] + right[0] + box_w) / 2
            label_y = (left[1] + right[2]) / 2
            ax.text(label_x, label_y, f"{champ_name}", fontsize=9, fontweight='bold', ha='center', va='center')

    place_conference_label(east_team_boxes, east_final_round, f"Eastern Conference Champion:\n{east_champ}")
    place_conference_label(west_team_boxes, west_final_round, f"Western Conference Champion:\n{west_champ}")

    # Draw Finals
    finals_x = 15
    finals_y = (y_east + y_west) / 2

    ax.text(finals_x, finals_y + 6, "Finals", fontsize=14, weight='bold', ha='center')

    team1, team2, champ = finals
    norm_team1 = normalize(team1)
    norm_team2 = normalize(team2)
    norm_champ = normalize(champ)

    color_final_1 = 'red' if norm_highlight == norm_team1 else 'black'
    color_final_2 = 'red' if norm_highlight == norm_team2 else 'black'
    color_champ = 'red' if norm_highlight == norm_champ else 'black'

    ax.text(finals_x, finals_y + 5, f"{team1} vs {team2}", fontsize=10, ha='center',
            color='red' if norm_highlight in [norm_team1, norm_team2] else 'black')
    ax.text(finals_x, finals_y + 4.25, f"Winner: {champ}", fontsize=10, fontweight='bold',
            ha='center', color=color_champ)

    plt.tight_layout()
    return fig