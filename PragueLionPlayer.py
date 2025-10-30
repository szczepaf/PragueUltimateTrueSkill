import json

class PragueLionPlayer:
    """A class for representing one individual player (do not interchange this with the Player class from the TrueSkillThroughTime library).

    Attributes:

    name: the player's name used in the scoring records.
    mu: the player's TrueSkill mean rating.
    sigma: the player's TrueSkill deviation.
    number_of_games: number of practices (games) played by the given player.
    """
    
    name: str
    mu: float
    sigma: float
    number_of_games: int = 0
    learning_curve: list = []
    k: float = 3 # uncertainty factor, the default is usually 3

    def __init__(self, name: str, learning_curve, mu: float = 25, sigma: float = (28/3), number_of_games: int = 0) -> None:
        """Initialize the PragueLionPlayer with a name, mu, sigma, and number of games played.
        Use default TrueSkill starting values for mu and sigma.
        Compute True Skill as mu - k * sigma.
        """
        self.name = name
        self.mu = mu
        self.sigma = sigma
        self.learning_curve = learning_curve
        self.number_of_games = number_of_games
        self.true_skill = mu - self.k * sigma


    def __str__(self) -> str:
        """
        Return a stable string dump of all fields as a string.     
        """
        return f"{self.name},{self.number_of_games},{self.true_skill:.6f},{self.mu:.6f},{self.sigma:.6f}"       

    def plot_learning_curve(self):
        """Plot the learning curve of the player using matplotlib."""
        # TODO: implement plotting
        pass
    
