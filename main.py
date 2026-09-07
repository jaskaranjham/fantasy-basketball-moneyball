import re
import pandas as pd

all_players = []
seen_names = set()

for page_number in range(1, 11):
    print("Downloading ESPN page", page_number)

    espn_url = (
        "https://www.espn.com/nba/stats/player/"
        f"_/page/{page_number}"
    )

    tables = pd.read_html(espn_url)

    names_table = tables[0]
    stats_table = tables[1]

    page_players = pd.concat(
        [names_table[["Name"]], stats_table],
        axis=1
    )

    new_players = page_players[
        ~page_players["Name"].isin(seen_names)
    ]

    if new_players.empty:
        break

    all_players.append(new_players)
    seen_names.update(new_players["Name"])

players = pd.concat(
    all_players,
    ignore_index=True
)

print("Total players downloaded:", len(players))
team_codes = [
    "ATL", "BOS", "BKN", "CHA", "CHI", "CLE", "DAL", "DEN",
    "DET", "GS", "HOU", "IND", "LAC", "LAL", "MEM", "MIA",
    "MIL", "MIN", "NO", "NY", "OKC", "ORL", "PHI", "PHX",
    "POR", "SAC", "SA", "TOR", "UTA", "UTAH", "WSH"
]

team_pattern = "|".join(
    sorted(team_codes, key=len, reverse=True)
)


def separate_name_and_team(combined_name):
    match = re.search(
        rf"((?:{team_pattern})(?:/(?:{team_pattern}))*)$",
        combined_name
    )

    if match:
        player_name = combined_name[:match.start()]
        team = match.group()
        return pd.Series([player_name, team])

    return pd.Series([combined_name, "Unknown"])


players[["Name", "Team"]] = players["Name"].apply(
    separate_name_and_team
)

players["Fantasy PPG"] = (
    players["PTS"]
    + (players["FGM"] * 2)
    - players["FGA"]
    + players["FTM"]
    - players["FTA"]
    + players["3PM"]
    + players["REB"]
    + (players["AST"] * 2)
    + (players["STL"] * 4)
    + (players["BLK"] * 4)
    - (players["TO"] * 2)
)

players["Fantasy PPG"] = players["Fantasy PPG"].round(2)

#FILTER
players = players[
    (players["GP"] >= 20)
    & (players["MIN"] >= 15)
    ].copy()

players["Fantasy Points Per Minute"] = (
        players["Fantasy PPG"] / players["MIN"]
).round(3)

players["Fantasy Points Per 36"] = (
        players["Fantasy Points Per Minute"] * 36
).round(2)

players["Scoring Contribution"] = (
        players["PTS"]
        + (players["FGM"] * 2)
        - players["FGA"]
        + players["FTM"]
        - players["FTA"]
        + players["3PM"]
).round(2)

players["Rebounding Contribution"] = (
    players["REB"]
).round(2)

players["Playmaking Contribution"] = (
        (players["AST"] * 2)
        - (players["TO"] * 2)
).round(2)

players["Defensive Contribution"] = (
        (players["STL"] * 4)
        + (players["BLK"] * 4)
).round(2)
#END OF FILTER
contribution_columns = [
    "Scoring Contribution",
    "Rebounding Contribution",
    "Playmaking Contribution",
    "Defensive Contribution"
]

percentile_columns = []

for contribution in contribution_columns:
    percentile_name = contribution.replace(
        "Contribution",
        "Percentile"
    )

    players[percentile_name] = (
        players[contribution]
        .rank(pct=True)
        .mul(100)
        .round(2)
    )

    percentile_columns.append(percentile_name)

players["Fantasy PPG Percentile"] = (
    players["Fantasy PPG"]
    .rank(pct=True)
    .mul(100)
    .round(2)
)

players["Across-the-Board Score"] = (
        4 / sum(
    1 / players[column].clip(lower=1)
    for column in percentile_columns
)
).round(2)

players["Maximum Value Score"] = (
        (players["Fantasy PPG Percentile"] * 0.70)
        + (players["Across-the-Board Score"] * 0.30)
).round(2)

players["Fantasy PPG Rank"] = (
    players["Fantasy PPG"]
    .rank(method="min", ascending=False)
    .astype(int)
)

players["Maximum Value Rank"] = (
    players["Maximum Value Score"]
    .rank(method="min", ascending=False)
    .astype(int)
)

draft_board = players.sort_values(
    by="Maximum Value Rank"
)

columns_to_show = [
    "Maximum Value Rank",
    "Fantasy PPG Rank",
    "Name",
    "Team",
    "POS",
    "GP",
    "MIN",
    "Fantasy PPG",
    "Maximum Value Score",
    "Across-the-Board Score",
    "Scoring Percentile",
    "Rebounding Percentile",
    "Playmaking Percentile",
    "Defensive Percentile",
    "Scoring Contribution",
    "Rebounding Contribution",
    "Playmaking Contribution",
    "Defensive Contribution",
    "PTS",
    "REB",
    "AST",
    "STL",
    "BLK",
    "TO"
]

final_board = draft_board[columns_to_show]

print(final_board.head(25))

final_board.to_excel(
    "fantasy_draft_board_v1.xlsx",
    sheet_name="Maximum Value Board",
    index=False
)

print("\nV1 Maximum Value Board exported!")