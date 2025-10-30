import csv
import os
import pandas
from trueskillthroughtime import *
import random
import matplotlib.pyplot as plt

import pandas as pd
import PragueLionPlayer

GAMES_DB_PATH = "games_db.csv"

def parse_team(team_string: str) -> list[str]:
    """Parse a team string into a list of player names as strings.

    The input format is: "[Alice|Bob|Charlie]".
    """
    if not team_string:
        return []

    stripped = team_string.strip()

    if stripped.startswith("[") and stripped.endswith("]"):
        cleared = stripped[1:-1].strip()

    if not cleared: # empty team
        return []

    # Split on | and trim whitespace from each name
    names = [part.strip() for part in cleared.split("|")]
    # Filter out accidental empty strings, return the names
    return [n for n in names if n]



def load_all_player_names() -> list[str]:
    """Load all unique player names from the games database CSV file.

    The CSV is expected to have columns 'winning_team' and 'losing_team'
    where each team is stored as a bracketed, '|' separated list, e.g.:
        [Frnda|Xnapy|Scoot]
    """
    df = pandas.read_csv(GAMES_DB_PATH)

    player_names: set[str] = set()

    for team_col in ("winning_team", "losing_team"):
        for team_string in df[team_col]:
            for name in parse_team(team_string):
                player_names.add(name)

    # Return a sorted list for reproducibility
    # TODO: check against an allowed file of player names for types and disallowed names
    return sorted(player_names)

def get_attendance_count_for_player(prague_lion_player: PragueLionPlayer, games_df: pd.DataFrame) -> int:
    """Count how many attendences a player has attended based on the df with games.
    Attendences differ from games played, as one practice session may have multiple games.
    Attendences are counted as the number of unique dates a player has played on."""
    return 0
    #TODO: implement attendance counting logic

def parse_game_row(row: dict) -> list:
    """Parse a single row from the games database into TTT's composition format.

    TrueSkill Through Time's History accepts a composition list where
    each element is a list of two or more teams, and the order implies
    the result: the first team beat the later team(s).

    So we return:
        [ winning_team_list, losing_team_list ]

    TODO: draws
    """
    winning = parse_team(row["winning_team"])
    losing = parse_team(row["losing_team"])
    return [winning, losing]


def get_players_ratings(history: History, player_names: list) -> dict[str, tuple[float, float]]:
    """Fetch the final rating of players from the game history, consisting of mean and variance.
    The ratings are returned in a dict keyed by the player names."""
    history.convergence() # calculate final ratings by TrueSkill Through Time
    # TODO: check if default params for the method above should be adjusted
    ratings = dict()
    for player_name in player_names:
        player_curve = history.learning_curves()[player_name]
        final_rating = player_curve[-1][1] # get the last Gaussian object corresponding to the player's final rating
        ratings[player_name] = (final_rating.mu, final_rating.sigma) # get the mean and std deviation

    return ratings


def initialize_players_and_fetch_their_ratings_and_attendance(player_names, games_df):
    """Read the game data from the source file, initialize players as the PragueLionPlayer class,
    and fetch their ratings and attendance count."""
    games = []
    for _, row in games_df.iterrows():
        game = parse_game_row(row)
        weight = row.get("weight", 1) # TODO: use weights to make RedZone games more important?
        games.append(game)
    game_history = History(composition=games) # TODO: any important params?
    player_ratings = get_players_ratings(game_history, player_names)

    prague_lion_players = []

    for name in player_names:
        mu, sigma = player_ratings[name]
        current_learning_curve = game_history.learning_curves()[name]
        prague_lion_player = PragueLionPlayer.PragueLionPlayer(name, current_learning_curve, mu, sigma)
        prague_lion_players.append(prague_lion_player)

    return prague_lion_players


def dump_leaderboard(prague_lion_players: list[PragueLionPlayer], outputfile: str):
    """
    Dump the players in TrueSkill order to csv.
    Columns: name, rank, true_skill, mu, sigma, games
    """
    # Sort: by true_skill desc, then by name asc for stable ordering
    players_sorted = sorted(
        prague_lion_players,
        key=lambda p: (-p.true_skill, p.name.lower())
    )

    # Write CSV
    with open(outputfile, "w", encoding="utf-8", newline="") as f:
        f.write("name,rank,true_skill,mu,sigma,games\n")
        for idx, player in enumerate(players_sorted, start=1):
            f.write(f"{player.name},{idx},{player.true_skill:.6f},{player.mu:.6f},{player.sigma:.6f},{player.number_of_games}\n")


def main():
    """Main function to load and parse the games database."""
    player_names = load_all_player_names()
    print("Unique Player Names:", player_names)

    # Load the games dataframe
    games_df = pandas.read_csv(GAMES_DB_PATH)
    
    prague_lion_players = initialize_players_and_fetch_their_ratings_and_attendance(player_names, games_df)
    dump_leaderboard(prague_lion_players, "leaderboard.csv")


if __name__ == "__main__":
    main()


