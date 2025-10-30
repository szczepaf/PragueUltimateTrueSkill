import csv
import os
import pandas
from trueskillthroughtime import *
import random
import matplotlib.pyplot as plt

GAMES_DB_PATH = "games_db.csv"

def parse_team(team_string) -> list[str]:
    """Parse a team string into a list of player names.

    The input format is expected like: "[Alice|Bob|Charlie]".
    Robust to extra whitespace and empty items.
    """
    if team_string is None:
        return []

    stripped = str(team_string).strip()

    if stripped.startswith("[") and s.endswith("]"):
        cleared = s[1:-1].strip()

    if not cleared: # empty team
        return []

    # Split on | and trim whitespace from each name
    names = [part.strip() for part in cleared.split("|")]
    # Filter out any accidental empty strings
    return [n for n in names if n]



def load_all_player_names() -> list[str]:
    """Load all unique player names from the games database CSV file.

    The CSV is expected to have columns 'winning_team' and 'losing_team'
    where each team is stored as a bracketed, '|' separated list, e.g.:
        [Frnda|Xnapy|Scoot]
    """
    df = pandas.read_csv(GAMES_DB_PATH)

    players: set[str] = set()

    for team_col in ("winning_team", "losing_team"):
        for team_string in df[team_col]:
            for name in parse_team(team_string):
                players.add(name)

    # Return a sorted list for reproducibility
    # TODO: check against an allowed file of player names for types and disallowed names
    return sorted(players)

def get_attendance_count_for_player(prague_lion_player: PragueLionPlayer, games_df: pd.DataFrame) -> int:
    """Count how many games a player has attended based on the games dataframe."""
    attendance_count = 0
    return 0
    #TODO: implement attendance counting logic

def parse_game_row(row: dict) -> list:
    """Parse a single row from the games database into TTT's composition format.

    TrueSkill Through Time's History accepts a 'composition' list where
    each element is a list of two (or more) teams, and the order implies
    the result: the first team beat the later team(s).

    For our two-team case, we return:
        [ winning_team_list, losing_team_list ]

    TODO: draws
    """
    winning = parse_team(row["winning_team"])
    losing = parse_team(row["losing_team"])
    return [winning, losing]


def get_players_ratings(history, player_names: list) -> dict[str, tuple[float, float]]:
    """Get the final rating of players from the game history, consisting of mean and variance.
    They are stored in a dict by their names."""
    history.convergence() # calculate final ratings by TrueSkill Through Time
    ratings = dict()
    for player_name in player_names:
        player_curve = history.learning_curves()[player_name]
        final_rating = player_curve[-1][1] # get the last Gaussian object
        ratings[player_name] = (final_rating.mu, final_rating.sigma) # get the mean and std deviation

    return ratings


def initialize_players_and_fetch_their_ratings_and_attendance(player_names, games_df):
    """Read the game data from the source file, initialize players as the PragueLionPlayer class,
    and fetch their ratings and attendance count."""
    games = [parse_game_row(row) for _, row in games_df.iterrows()]
    game_history = History(composition=games)
    player_ratings = get_players_ratings(game_history, player_names)

    prague_lion_players = []

    for name in player_names:
        mu, sigma = player_ratings[name]
        current_learning_curve = game_history.learning_curves()[name]
        prague_lion_player = PragueLionPlayer(name, current_learning_curve, mu, sigma)
        prague_lion_players.append(prague_lion_player)

    return prague_lion_players


def present_leaderboard(prague_lion_players: list[PragueLionPlayer], outputfile: str):
    """Dump the players into an output file, sorted by their true skill."""
    pass


def main(uncertainty_factor: float = 2.0):
    """Main function to load and parse the games database."""
    player_names = load_all_player_names()
    print("Unique Player Names:", player_names)

    # Load the games dataframe
    games_df = pandas.read_csv(GAMES_DB_PATH)
    
    prague_lion_players = initialize_players_and_fetch_their_ratings_and_attendance(player_names, games_df)
    present_leaderboard(prague_lion_players, "leaderboard.txt")

main()


